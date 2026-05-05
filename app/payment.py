import razorpay

RAZORPAY_KEY = "rzp_test_xxxxx"
RAZORPAY_SECRET = "your_secret_here"

client = razorpay.Client(auth=(RAZORPAY_KEY, RAZORPAY_SECRET))