from django.shortcuts import render
from .models import Bedrock, Request, Advice, RawAdvice, Cost
from .bedrock import Bedrock as AWS_Bedrock
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator


# @cache_page(60 * 60 * 24 * 14)
def not_fin_advice(request):
    return render(request, "not-fin-advice.html")


def approximate_cost(
    in_text_char_count, out_text, in_token_price=0.00163, out_token_price=0.00551
):
    # price is per 1000 token
    # the padding is the chars i use for the actuall command
    in_tokens = in_text_char_count / 4
    out_tokens = len(out_text) / 4

    in_cost = (in_tokens / 1000) * in_token_price
    out_cost = (out_tokens / 1000) * out_token_price

    return {
        "in": in_cost,
        "out": out_cost,
        "total": in_cost + out_cost,
        "in_char_count": in_text_char_count,
        "in_token_count": in_tokens,
        "out_char_count": len(out_text),
        "out_token_count": out_tokens,
        "in_token_price": in_token_price,
        "out_token_price": out_token_price,
    }


def index(request):
    char_limit = 2000

    requests_list = Request.objects.all().order_by("-id")
    paginator = Paginator(requests_list, 10)  # Show 25 contacts per page.
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "max_question_length": char_limit,
        "max_token_length": int(char_limit / 4),
        "page_obj": page_obj,
    }
    return render(request, "index.html", context)


@require_POST
def advice(request):
    qmax = 2000
    if request.method == "POST":
        question = request.POST.get("question_text")
        selector = request.POST.get("answer-style-select")
        checkbox = request.POST.get("not-fin-advice-checkbox")

        # missing style
        style_choices = ["dumb", "pro", "wsb"]
        if not selector or selector not in style_choices:
            response_data = {"error": "No style was selected"}
            return JsonResponse(response_data, status=400)

        # missing checkbox
        if not checkbox or checkbox != "on":
            response_data = {"error": "Did not accept financial advice checkobx."}
            return JsonResponse(response_data, status=400)

        # no question
        if not question:
            response_data = {"error": "Missing parameter: question"}
            return JsonResponse(response_data, status=400)

        # question too long
        if len(question) > qmax:
            response_data = {
                "error": f"Question too big was {len(question)} and max is {qmax}"
            }
            return JsonResponse(response_data, status=400)

        # question was already asked
        if Request.objects.filter(text=question, mode=selector).exists():
            last_advice = Request.objects.filter(text=question, mode=selector).last()

            return JsonResponse(
                {
                    "question": last_advice.text,
                    "mode": last_advice.mode,
                    "raw": last_advice.raw_finadvice.raw_text,
                    "cost": Cost.objects.get(request=last_advice).total_cost,
                },
                status=200,
            )

        # new question
        ai = AWS_Bedrock()
        output = ai.learn(description=question, style=selector)

        # article = ai.article(output)

        raw_fin_id = RawAdvice.objects.create(raw_text=output["ai_response"])

        # leaving empty for now, need to parse repsonse first etc
        fin_id = Advice.objects.create(markdown="", excerpt="")

        raw_fin_id = RawAdvice.objects.create(raw_text=output["ai_response"])

        request_obj = Request.objects.create(
            mode=selector,
            finadvice=fin_id,
            raw_finadvice=raw_fin_id,
            text=question,
        )

        cost_dict = approximate_cost(output["char_count"], output["ai_response"])

        cost_obj = Cost.objects.create(
            request=request_obj,
            current_in_price=cost_dict["in_token_price"],
            current_out_price=cost_dict["out_token_price"],
            in_cost=cost_dict["in"],
            out_cost=cost_dict["out"],
            total_cost=cost_dict["total"],
            in_char_count=cost_dict["in_char_count"],
            out_char_count=cost_dict["out_char_count"],
            in_token_count=cost_dict["in_token_count"],
            out_token_count=cost_dict["out_token_count"],
        )

        raw_resp_data = {
            "question": request_obj.text,
            "mode": request_obj.mode,
            "raw": raw_fin_id.raw_text,
            "cost": cost_obj.total_cost,
        }
        return JsonResponse(raw_resp_data, status=200)

        # response_data = {"response": "asking the big ai in the cloud, please hold."}


def like_answer(request, new_comment):
    if request.session.get("has_commented", False):
        return HttpResponse("You've already commented.")
    c = comments.Comment(comment=new_comment)
    c.save()
    request.session["has_commented"] = True
    return HttpResponse("Thanks for your comment!")


def like_question(request, new_comment):
    if request.session.get("has_commented", False):
        return HttpResponse("You've already commented.")
    c = comments.Comment(comment=new_comment)
    c.save()
    request.session["has_commented"] = True
    return HttpResponse("Thanks for your comment!")
