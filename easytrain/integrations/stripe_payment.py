import stripe

from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class StripePayment:
    
    def __init__(self, amount):
        self.amount = amount
    
    def create_one_time_price(self):
        try:
            product_id = self.create_product("EasyTrain Purchase").stripe_id

            price = stripe.Price.create(
                unit_amount=self.amount,
                currency="usd",
                product=product_id
            )
            return price.stripe_id
        except stripe.error.StripeError as e:
            print(f"Stripe Error: {e}")
        except Exception as e:
            print(f"Error: {e}")

    def create_product(self, name):
        try:
            product = stripe.Product.create(
                name=name,
                description="EasyTrain Bill payment for one time purchase",
                type="service",  # or "good" for a physical product
            )
            return product
        except stripe.error.StripeError as e:
            # Handle any Stripe-specific errors
            print(f"Stripe Error: {e}")
        except Exception as e:
            # Handle any other errors
            print(f"Error: {e}")

    def checkout_session(self):
        stripe_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price": str(self.create_one_time_price()),
                    "quantity": 1
                }
            ],
            mode="payment",
            success_url="http://staging-env-easytrain.eba-syvqgi3q.us-west-2.elasticbeanstalk.com/api/payment_success/",
            cancel_url="http://staging-env-easytrain.eba-syvqgi3q.us-west-2.elasticbeanstalk.com/api/payment_failed/",
        )
        return stripe_session
