import 'package:flutter/material.dart';
import 'signup_page.dart';
import 'home_page.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {

  final _formKey = GlobalKey<FormState>();

  final TextEditingController username = TextEditingController();
  final TextEditingController password = TextEditingController();

  void login() {

    if (_formKey.currentState!.validate()) {

      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (context) => const HomePage(),
        ),
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

                        /// LOGO
                        Image.asset(
                          "assets/logo1.png",
                          height: 170,
                        ),

                        const SizedBox(height: 25),

                        /// USERNAME
                        TextFormField(
                          controller: username,

                          decoration: InputDecoration(
                            hintText: "Username",
                            prefixIcon: const Icon(Icons.person),

                            filled: true,
                            fillColor: Colors.grey.shade200,

                            border: OutlineInputBorder(
                              borderRadius: BorderRadius.circular(30),
                              borderSide: BorderSide.none,
                            ),
                          ),

                          validator: (value) {

                            if (value == null || value.isEmpty) {
                              return "Username is required";
                            }

                            return null;
                          },
                        ),

                        const SizedBox(height: 20),

                        /// PASSWORD
                        TextFormField(
                          controller: password,
                          obscureText: true,

                          decoration: InputDecoration(
                            hintText: "Password",
                            prefixIcon: const Icon(Icons.lock),

                            filled: true,
                            fillColor: Colors.grey.shade200,

                            border: OutlineInputBorder(
                              borderRadius: BorderRadius.circular(30),
                              borderSide: BorderSide.none,
                            ),
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

                        const SizedBox(height: 25),

                        /// LOGIN BUTTON
                        SizedBox(
                          width: double.infinity,
                          height: 55,

                          child: ElevatedButton(
                            onPressed: login,

                            style: ElevatedButton.styleFrom(
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(30),
                              ),
                              padding: EdgeInsets.zero,
                            ),

                            child: Ink(
                              decoration: const BoxDecoration(
                                gradient: LinearGradient(
                                  colors: [
                                    Color(0xff00C9A7),
                                    Color(0xff007CF0),
                                  ],
                                ),
                                borderRadius:
                                BorderRadius.all(Radius.circular(30)),
                              ),

                              child: const Center(
                                child: Text(
                                  "LOG IN",
                                  style: TextStyle(
                                    fontWeight: FontWeight.bold,
                                    fontSize: 16,
                                  ),
                                ),
                              ),
                            ),
                          ),
                        ),

                        const SizedBox(height: 20),

                        /// SIGNUP LINK
                        Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [

                            const Text("Not a member? "),

                            GestureDetector(
                              onTap: () {

                                Navigator.push(
                                  context,
                                  MaterialPageRoute(
                                    builder: (context) => const SignupPage(),
                                  ),
                                );

                              },

                              child: const Text(
                                "Sign up now",
                                style: TextStyle(
                                  color: Colors.blue,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            )
                          ],
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