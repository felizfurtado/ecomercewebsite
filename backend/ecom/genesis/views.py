from django.shortcuts import render
from django.http import HttpResponse
import json
from django.shortcuts import redirect
from .models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
import uuid 


def home(request):
    user_name = None
    user_id = request.session.get('user_id')
    session_token = request.session.get('user_token')
    url_token = request.GET.get('token')

    if user_id and session_token and not url_token:
        return redirect(f'/home/?token={session_token}')

    if user_id and session_token == url_token:
        user = Users.objects.filter(id=user_id).first()
        if user:
            user_name = user.fullname
    set1=[]
    set2=[]

    with open("genesis/templates/product.json", "r") as file:
        products = json.load(file)
        set1 = products[:3] 
        set2 = products[3:6]


    for i in set2:
        print(i["title"])

    return render(request, 'index.html', {'user_name': user_name , 'set1': set1 , 'set2': set2 , "cart": request.session['cc']})


def shop(request):
    user_name = None
    user_id = request.session.get('user_id')
    session_token = request.session.get('user_token')
    url_token = request.GET.get('token')


    if user_id and session_token and not url_token:
        return redirect(f'/shop/?token={session_token}')

    if user_id and session_token == url_token:
        user = Users.objects.filter(id=user_id).first()
        if user:
            user_name = user.fullname

    prod = []
    with open("genesis/templates/product.json", "r") as file:
        products = json.load(file)
        prod = products

    if request.method == "POST":

        categories = request.POST.getlist('category')
        price = request.POST.get('price') 
        color = request.POST.get('color')
        print(categories , price , color)
       

        filtered_prod =  []
        filtered_prod_id =  []

        extra_id =[]
        temp_filtered_prod_id = []




        for i in prod:


            if categories:    
                if i['meta']['category'].lower() in categories:
                    # filtered_prod.append(i)
                    
                    filtered_prod_id.append(i['id'])
                else:
                    extra_id.append(i['id'])
            else:
                error_message = "Sorry, there are no products matching your search criteria."
                return render(request, 'shop.html', {"error_message":error_message})


            if price:
                product_price = i['price']['current']
                print(f"Checking product {i['id']} with price {product_price}")

                if float(price)>=float(product_price):
                    filtered_prod_id.append(i['id']) 
                    temp_filtered_prod_id.append(i['id']) 
                    print(f"Added to temp_filtered_prod_id: {temp_filtered_prod_id}")

                else:
                    extra_id.append(i["id"])
                    print(f"Added to extra_id: {set(extra_id)}")

            if color:
                found_color = False
                for c in i["options"]["colors"]:
                    if c["name"].lower() == color.lower():
                        found_color = True
                        break
                    
                if found_color:
                    filtered_prod_id.append(i['id'])
                else:
                    extra_id.append(i['id'])

                


            

        if not temp_filtered_prod_id:
            error_message = "Sorry, there are no products matching your search criteria."
            return render(request, 'shop.html', {"error_message": error_message})

        for i in prod:
            if filtered_prod_id:
                if i['id'] in filtered_prod_id and i['id'] not in extra_id:
                    filtered_prod.append(i)



        
        request.session['filtered_prod'] = filtered_prod

        return redirect(f'/shop/?token={session_token}')
    

    filtered_prod = request.session.pop('filtered_prod', None)
    if filtered_prod:
        prod = filtered_prod
            

    return render(request, 'shop.html', {'user_name': user_name , 'prod': prod,"cart": request.session['cc'] })



def product_view(request):
    user_name = None
    user_id = request.session.get('user_id')
    session_token = request.session.get('user_token')
    url_token = request.GET.get('token')
    title = request.GET.get("title")
    alert_message = ""
    success_message = ""

    if 'cc' not in request.session:
        request.session['cc'] = 0
    

    if user_id and session_token == url_token:
        user = Users.objects.filter(id=user_id).first()
        if user:
            user_name = user.fullname


    with open("genesis/templates/product.json", "r") as file:
        product = json.load(file)
        for i in product:
            if i["title"] == title:
                product = i
                break

        print("Product Title:", product["title"])  
 

    if request.method == "POST":

        ti = request.POST.get("ti")
        image = request.POST.get('image')
        price = request.POST.get('price')
        selected_color = request.POST.get("selectedcolor")
        selected_size = request.POST.get("selectedsize")
        prod_cart_count = 1
        cart_prod = request.session.get('cart_prod',[])
        total = request.session.get('total', 0)
        new_id = len(cart_prod) + 1

        print(ti)
        print(image)
        print(selected_color)
        print(selected_size)


        if selected_color and selected_size:
            request.session['cc']+=1
            print(request.session['cc'])


            item_found = False

            for item in cart_prod:
                if item['title']==ti and item['color'] == selected_color and item['size']== selected_size:
                    item['count']+=1
                    item_found = True
                    break
            

            if item_found == False:
                product_data = {
                    'id': new_id,
                    'title': ti,
                    'color':selected_color,
                    'size':selected_size,
                    'count':int(prod_cart_count),
                    'image': image,
                    'price':float(price)
                }
                cart_prod.append(product_data)

            request.session['cart_prod']=cart_prod
            print(request.session['cart_prod'])

            total=0
            for i in cart_prod:
                total += float(i['price']) * i['count']

            print('Total :', total)
            request.session['total'] = total

            success_message = ti+ " added in the cart"
            
        else:
            alert_message = "Oops! Looks like you missed picking a color and size. Please choose both to continue."
           

    return render(request, 'shop_single.html', {'user_name': user_name , 'product': product , "cart": request.session['cc'] , 'alert': alert_message , 'success' : success_message})



def cart(request):
    user_name = None
    user_id = request.session.get("user_id")
    session_token = request.session.get("user_token")
    url_token = request.GET.get("token")
    total = request.session.get('total')
    error_message=''

    # print("TOTAL :",total)
    if user_id and session_token == url_token:
        user = Users.objects.filter(id=user_id).first()
        if user:
             user_name = user.fullname
        cc = request.session.get("cc")
        cart_prod = request.session.get("cart_prod")
        print(cart_prod)
        print(cc)

    if request.method == "POST":
        cart_prod = request.session.get("cart_prod", [])
        ti = request.POST.get("title")
        selected_color = request.POST.get("selectedcolor")
        selected_size = request.POST.get("selectedsize")
        cc = request.session.get("cc")
        id =  request.POST.get("item_id")
        print('id : ', id)


        print(f"title: {ti}, color: {selected_color}, size: {selected_size}")


        for item in cart_prod:
            if item["title"] == ti and item['color'] == selected_color and item['size'] == selected_size :

                if 'dec' in request.POST:
                    if item['count'] > 1:
                        item['count']-=1
                        total=total-item["price"]
                        request.session['cc']-=1
                    else:
                        error_message = "Quantity cannot be less than 1."

                    print("Dec :", item['count'])

                elif 'inc' in request.POST:
                    item['count']+=1
                    total=total+item["price"]
                    request.session['cc']+=1
                    print("Inc :", item['count'])

                elif 'remove' in request.POST:
                    total -= item['price'] * item['count']  # subtract full cost of that item
                    request.session['cc'] -= item['count']  # adjust cart count accordingly
                    cart_prod.remove(item)
                    print("Removed :", item)



        request.session["cart_prod"]=cart_prod
        request.session["total"]=total

    return render(request , "cart.html", {'user_name':user_name , 'cart':cc , 'cart_prod': cart_prod , 'total':total , 'error_message':error_message})



def checkout(request):

    user_name = None
    user_id = request.session.get("user_id")
    session_token = request.session.get("user_token")
    url_token = request.GET.get("token")
    total = request.session.get('total')
    error_message=''

    # print("TOTAL :",total)
    if user_id and session_token == url_token:
        user = Users.objects.filter(id=user_id).first()
        if user:
             user_name = user.fullname
        cc = request.session.get("cc")
        cart_prod = request.session.get("cart_prod")
        print(cart_prod)
        print(cc)

    if request.method == "POST":
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")
        address2 = request.POST.get("address2")
        city = request.POST.get("city")
        zipcode = request.POST.get("zip")
        country = request.POST.get("country")
        status="Pending"
        print(email)

        order_data = {
    'email': email,
    'phone': phone,
    'first_name': first_name,
    'last_name': last_name,
    'address': address,
    'address2': address2,
    'city': city,
    'zip': zipcode,
    'country': country,
    'cart':cart_prod,
    'status':status

}
        

        

        with open ("genesis/templates/orders.json" , mode="r") as f:
            try:
                orders = json.load(f)
            except json.JSONDecodeError:
                orders = []

        orders.append(order_data)

        with open ("genesis/templates/orders.json" , mode="w") as f:
            json.dump(orders ,f , indent=4)

    return render (request , 'checkout.html', {'user_name':user_name , 'cart':cc , 'cart_prod': cart_prod , 'total':total , 'error_message':error_message})

def about(request):
    user_name = None
    user_id = request.session.get("user_id")
    session_token = request.session.get("user_token")
    url_token = request.GET.get("token")
    if user_id and session_token == url_token:
        user = Users.objects.filter(id=user_id).first()
        if user:
            user_name = user.fullname  
    

    return render(request, "about.html", {"user_name": user_name , 'cart':request.session['cc']})


def login(request):
    alert_message = ""

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        print("Email:", email)  
        print("Password:", password)  
        user = Users.objects.filter(email=email).first()
        if user and check_password(password, user.password):
            request.session['user_id'] = user.id
            request.session.set_expiry(60 * 60 * 24 * 5)
            print("Login successful")
            token = str(uuid.uuid4())
            request.session['user_token'] = token
            return redirect(f'/home/?token={token}')
        else:
            alert_message = "Invalid email or password."

    return render(request, 'login.html', {'alert_message': alert_message})


def clear_cc(request):
    if 'cc' in request.session:
        del request.session['cc']
        del request.session['cart_prod']
        del request.session['total']
    return redirect('shop') 


def logout_view(request):

    request.session.flush()

    return redirect('login')


def admin_check(request):

    with open ("genesis/templates/orders.json" , mode="r") as f:
        total_orders = json.load(f)

    total = request.session.get("total")

    for i in total_orders:
        items = len(i['cart'])
        print(items)

    if request.method =="POST":
        id = request.POST.get("id")
        print(id)

    return render(request ,'admin.html' ,{'total_orders' : total_orders , "total":total , 'items':items})


def admin_view(request):

    with open ("genesis/templates/orders.json" , mode="r") as f:
        total_orders = json.load(f)

    total = request.session.get("total")
    item = None
    
    if request.method =="POST":
        email = request.POST.get("email")
        print(email)
        
        for i in total_orders:
            if email == i['email']:
                item = i
                break 

        if 'success' in request.POST:
            for i in total_orders:
                if email == i['email']:
                    i['status'] = "success"

       

        # 🔄 Save updated orders back to JSON
        with open("genesis/templates/orders.json", mode="w") as f:
            json.dump(total_orders, f, indent=2)

        print("Updated Order:", item)


    return render(request ,'admin_view.html' ,{ "total":total , 'item':item})


def signup(request):
    alert_message = ""
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        print("Full Name:", fullname)  

        if password != confirm_password:
            alert_message = "Passwords do not match."
        else:
            if Users.objects.filter(email=email).exists():
                alert_message = "Email already exists."
            else:
                Users.objects.create( 
                    fullname=fullname, 
                    email=email, 
                    password=make_password(password)
                    )
                
                print("User data saved to database.")
                return redirect('login')
    return render(request, 'signup.html', {'alert_message': alert_message})

        

