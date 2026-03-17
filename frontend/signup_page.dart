import 'package:flutter/material.dart';

class SignupPage extends StatefulWidget {
  const SignupPage({super.key});

  @override
  State<SignupPage> createState() => _SignupPageState();
}

class _SignupPageState extends State<SignupPage> {

  final _formKey = GlobalKey<FormState>();

  final TextEditingController username = TextEditingController();
  final TextEditingController email = TextEditingController();
  final TextEditingController password = TextEditingController();
  final TextEditingController confirmPassword = TextEditingController();

  void signup() {

    if (_formKey.currentState!.validate()) {

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Account Created Successfully")),
      );

    }

  }

  @override
  Widget build(BuildContext context) {

    return Scaffold(

      body: Container(

        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [
              Color(0xff1CB5E0),
              Color(0xff000851),
            ],
          ),
        ),

        child: Center(
          child: SingleChildScrollView(
            child: Padding(
              padding: const EdgeInsets.all(25),

              child: Card(
                elevation: 18,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(25),
                ),

                child: Padding(
                  padding: const EdgeInsets.all(25),

                  child: Form(
                    key: _formKey,

                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [

                        Image.asset("assets/logo1.png", height: 170),

                        const SizedBox(height: 20),

                        /// USERNAME
                        TextFormField(
                          controller: username,
                          decoration: InputDecoration(
                            hintText: "Username",
                            prefixIcon: const Icon(Icons.person),
                          ),

                          validator: (value) {

                            if (value == null || value.isEmpty) {
                              return "Username is required";
                            }

                            return null;
                          },
                        ),

                        const SizedBox(height: 20),

                        /// EMAIL
                        TextFormField(
                          controller: email,
                          decoration: const InputDecoration(
                            hintText: "Email",
                            prefixIcon: Icon(Icons.email),
                          ),

                          validator: (value) {

                            if (value == null || value.isEmpty) {
                              return "Email is required";
                            }

                            if (!RegExp(r'\S+@\S+\.\S+').hasMatch(value)) {
                              return "Enter valid email";
                            }

                            return null;
                          },
                        ),

                        const SizedBox(height: 20),

                        /// PASSWORD
                        TextFormField(
                          controller: password,
                          obscureText: true,
                          decoration: const InputDecoration(
                            hintText: "Password",
                            prefixIcon: Icon(Icons.lock),
                          ),

                          validator: (value) {

                            if (value == null || value.isEmpty) {
                              return "Password is required";
                            }

                            if (value.length < 6) {
                              return "Password must be at least 6 characters";
                            }

                            return null;
                          },
                        ),

                        const SizedBox(height: 20),

                        /// CONFIRM PASSWORD
                        TextFormField(
                          controller: confirmPassword,
                          obscureText: true,
                          decoration: const InputDecoration(
                            hintText: "Confirm Password",
                            prefixIcon: Icon(Icons.lock),
                          ),

                          validator: (value) {

                            if (value != password.text) {
                              return "Passwords do not match";
                            }

                            return null;
                          },
                        ),

                        const SizedBox(height: 25),

                        GestureDetector(
                          onTap: signup,

                          child: Container(
                            width: double.infinity,
                            height: 55,

                            decoration: BoxDecoration(
                              gradient: const LinearGradient(
                                colors: [
                                  Color(0xff00C9A7),
                                  Color(0xff007CF0),
                                ],
                              ),

                              borderRadius: BorderRadius.circular(30),
                            ),

                            child: const Center(
                              child: Text(
                                "SIGN UP",
                                style: TextStyle(
                                  color: Colors.white,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ),
                          ),
                        ),

                        const SizedBox(height: 20),

                        GestureDetector(
                          onTap: () {
                            Navigator.pop(context);
                          },

                          child: const Text(
                            "Back to Login",
                            style: TextStyle(
                              color: Colors.blue,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        )
                      ],
                    ),
                  ),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}