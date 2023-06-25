import stripe
import urllib.parse

from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class StripePayment:
    
    def __init__(self, amount, customer):
        self.amount = amount
        self.customer = customer
    
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
    
    def create_customer(self):
        try:
            customer = stripe.Customer.create(
                email= self.customer.email,
                name= self.customer.name
            )
            return customer.id
        except stripe.error.StripeError as e:
            print(f"Stripe Error: {e}")
        except Exception as e:
            print(f"Error: {e}")

    def checkout_session(self):
        BASE_URL = "http://staging-env-easytrain.eba-syvqgi3q.us-west-2.elasticbeanstalk.com"
        # BASE_URL = "http://localhost:8000"
        success_url = BASE_URL + "/api/payment_success/"
        failure_url = BASE_URL + "/api/payment_failed/"



        # Encode the user's email and append it to the success URL as a query parameter
        encoded_email = urllib.parse.quote(self.customer.email)
        success_url_with_email = f"{success_url}?email={encoded_email}"

        stripe_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            customer=self.create_customer(),
            line_items=[
                {
                    "price": str(self.create_one_time_price()),
                    "quantity": 1
                }
            ],
            mode="payment",
            success_url=success_url_with_email,
            cancel_url=failure_url,
        )
        return stripe_session
