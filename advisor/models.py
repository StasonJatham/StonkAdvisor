from django.db import models


class Advice(models.Model):
    markdown = models.TextField()
    excerpt = models.TextField()

    def __str__(self):
        return


class RawAdvice(models.Model):
    raw_text = models.TextField()

    def __str__(self):
        return


class Request(models.Model):
    mode = models.CharField(max_length=5)  # wsb, pro, dumb
    finadvice = models.ForeignKey(Advice, on_delete=models.CASCADE)
    raw_finadvice = models.ForeignKey(RawAdvice, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    # md5_hash = models.CharField(max_length=32)

    def __str__(self):
        return


class Cost(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)

    current_in_price = models.FloatField()
    current_out_price = models.FloatField()

    in_cost = models.FloatField()
    out_cost = models.FloatField()
    total_cost = models.FloatField()

    in_char_count = models.IntegerField()
    out_char_count = models.IntegerField()

    in_token_count = models.IntegerField()
    out_token_count = models.IntegerField()

    def __str__(self):
        return


class Bedrock(models.Model):
    model = models.CharField(max_length=50)
    max_tokens_to_sample = models.IntegerField(default=2048)
    temperature = models.IntegerField(default=0)
    top_p = models.IntegerField(default=0)
    top_k = models.IntegerField(default=250)
    prompt = models.TextField()

    def __str__(self):
        return
