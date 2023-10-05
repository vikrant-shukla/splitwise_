from django.contrib.auth.models import User
from django.db.models import F
from rest_framework import serializers

from split.models import SplitAmount


class UserAmountSplitSerializer(serializers.Serializer):
    email = serializers.EmailField()
    amount = serializers.DecimalField(required=False, max_digits=8, decimal_places=2)
    percent = serializers.DecimalField(required=False, max_digits=3, decimal_places=1)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(f"Invalid email {value}.")

        return value


class SplitAmountSerializer(serializers.Serializer):
    total_amount = serializers.DecimalField(max_digits=8, decimal_places=2, min_value=1)
    split_type = serializers.ChoiceField(
        choices=[("EQUAL", "EQUAL"), ("PERCENT", "PERCENT"), ("EXACT", "EXACT")]
    )
    payer = serializers.EmailField()
    split_to = UserAmountSplitSerializer(many=True)

    class Meta:
        model = SplitAmount
        fields = "__all__"

    def validate_payer(self, value):
        """Validating the payer which is exists or not in the table"""

        if not User.objects.filter(email=value).exists():
            serializers.ValidationError("split owner not exist")
        return value

    def validate(self, attrs):
        """validating the percent is equally distributed or not"""

        if attrs.get("split_type") == "PERCENT":
            total_share = sum([i["percent"] for i in attrs.get("split_to")])
            if not total_share == 100:
                raise serializers.ValidationError(
                    "Total share percent is not equsl to 100%."
                )

        elif attrs.get("split_type") == "EXACT":
            """Validating the amount is exactly splitted into or not."""
            total_share = sum([i["amount"] for i in attrs.get("split_to")])
            if not total_share == attrs.get("total_amount"):
                raise serializers.ValidationError("Total share amount is wrong.")
        return attrs

    def split_payment(self, validated_data):
        """
        Overview: Function to seggerate the split amount based on different criteria mentioned i.e.
                  Equal, Exact, Percentage.
        param: validated data in which every element is present.
        """
        payer = validated_data["payer"]
        amount = validated_data["total_amount"]
        payee = validated_data["split_to"]
        split_type = validated_data["split_type"]
        payer = User.objects.get(email=payer)
        total_amount = amount

        if split_type == "EQUAL":
            amount = total_amount / len(payee)

            for data in payee:
                if data["email"] == payer:
                    continue

                owe_by = User.objects.filter(email=data["email"]).first()
                share_calc(owe_by=owe_by, payer=payer, amount=amount)

        if split_type == "EXACT":
            for data in payee:
                if data["email"] == payer.email:
                    continue

                owe_by = User.objects.filter(email=data["email"]).first()
                share_calc(owe_by=owe_by, payer=payer, amount=data["amount"])

        if split_type == "PERCENT":
            for data in payee:
                if data["email"] == payer.email:
                    continue

                amount = float(data["percent"] * total_amount) * (1 / 100)
                owe_by = User.objects.filter(email=data["email"]).first()
                share_calc(owe_by=owe_by, payer=payer, amount=amount)


def share_calc(owe_by: User, payer: User, amount: float) -> None:
    """
    Overview: Calculation logic to get who owe to whom and storing the data into respective table
    param: owe_by which is the person who owes the amount, payer is who pay the amount and
           amount is the given amount.
    """
    amount_share = SplitAmount.objects.filter(
        owe_from=owe_by, owe_by=payer, owe_amount__gt=0
    )
    if amount_share.exists():
        amount_share = amount_share.first()
        if amount_share.owe_amount > amount:
            amount_share.owe_amount = F("owe_amount") - amount
            amount_share.save(update_fields=("owe_amount",))
        else:
            amount = float(amount) - float(amount_share.owe_amount)
            amount_share = SplitAmount.objects.filter(owe_from=payer, owe_by=owe_by)
            if amount_share.exists():
                amount_share.update(owe_amount=amount)
            else:
                SplitAmount.objects.create(owe_from=payer, owe_by=owe_by, amount=amount)
            SplitAmount.objects.filter(owe_from=payer, owe_by=payer).update(amount=0)
    else:
        amount_share = SplitAmount.objects.filter(owe_from=payer, owe_by=owe_by)
        if amount_share.exists():
            amount_share.update(owe_amount=F("owe_amount") + amount)
        else:
            SplitAmount.objects.create(owe_from=payer, owe_by=owe_by, owe_amount=amount)


class SplitAmountToSerializer(serializers.ModelSerializer):
    owe_from_name = serializers.CharField(source="owe_from.get_full_name")
    owe_from = serializers.CharField(source="owe_from.email")
    owe_by_name = serializers.CharField(source="owe_by.get_full_name")
    owe_by = serializers.CharField(source="owe_by.email")

    class Meta:
        model = SplitAmount
        fields = "__all__"
