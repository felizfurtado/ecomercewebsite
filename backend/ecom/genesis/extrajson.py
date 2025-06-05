# def signup(request):
#     alert_message = ""
#     file_path = 'genesis/templates/signup.json'

#     if request.method == "POST":
#         fullname = request.POST.get('fullname')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         confirm_password = request.POST.get('confirm_password')

#         print("Full Name:", fullname)  

#         if password != confirm_password:
#             alert_message = "Passwords do not match."
#         else:
#             user_data = {
#                 'fullname': fullname,
#                 'email': email,
#                 'password': password,
#             }
#             try:
#                 with open(file_path, 'r') as f:
#                     existing_data = json.load(f)
                    
#             except (FileNotFoundError ,json.JSONDecodeError):
#                 existing_data = []

#             if type(existing_data) != list:
#                 existing_data = [existing_data]
            
#             existing_data.append(user_data)


#             try:
#                 with open(file_path, 'w') as f:
#                     json.dump(existing_data, f, indent=4)
#                     print("User data saved to JSON file.")


#             except Exception as e:
#                 print("Error saving JSON file:", e)
#                 alert_message = "Failed to save user data."

#             return redirect('login')

#     return render(request, 'signup.html', {'alert_message': alert_message})


# def login(request):
#     alert_message = ""

#     if request.method == "POST":
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         print("Email:", email)  
#         print("Password:", password)  

#         with open(file_path, 'r') as f:
#             data = json.load(f)
#             print("Data:", data)
#             for user in data:
#                 if user.get('email') == email and user.get('password') == password:
#                     print("Login successful")
#                     return redirect ('home')
#             print("Invalid credentials")
#             alert_message = "Invalid email or password."

#     return render(request, 'login.html', {'alert_message': alert_message})