import 'package:flutter/material.dart';

class PlantDetailsPage extends StatelessWidget {
  const PlantDetailsPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Plant Details"),
        backgroundColor: Colors.purple,
      ),
      body: const Center(
        child: Text(
          "Plant Details Screen",
          style: TextStyle(fontSize: 22),
        ),
      ),
    );
  }
}