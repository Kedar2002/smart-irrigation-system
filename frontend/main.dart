import 'package:flutter/material.dart';
import 'pages/login_page.dart';

void main() {
  runApp(const PlantBuddyApp());
}

class PlantBuddyApp extends StatelessWidget {
  const PlantBuddyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: "PlantBuddy",
      theme: ThemeData(
        primarySwatch: Colors.green,
      ),
      home: const LoginPage(),
    );
  }
}
