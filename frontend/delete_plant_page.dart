import 'package:flutter/material.dart';

class DeletePlantPage extends StatefulWidget {
  const DeletePlantPage({super.key});

  @override
  State<DeletePlantPage> createState() => _DeletePlantPageState();
}

class _DeletePlantPageState extends State<DeletePlantPage> {

  /// Temporary plant list (later fetched from database)
  List<Map<String, dynamic>> plants = [
    {"id": 1, "name": "Rose"},
    {"id": 2, "name": "Tulsi"},
    {"id": 3, "name": "Money Plant"},
  ];

  /// Delete Plant Function
  void deletePlant(int index) {

    showDialog(
      context: context,
      builder: (context) {

        return AlertDialog(

          title: const Text("Delete Plant"),

          content: Text(
            "Are you sure you want to delete ${plants[index]["name"]}?",
          ),

          actions: [

            TextButton(
              onPressed: () {
                Navigator.pop(context);
              },
              child: const Text("Cancel"),
            ),

            ElevatedButton(
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.red,
              ),

              onPressed: () {

                setState(() {
                  plants.removeAt(index);
                });

                Navigator.pop(context);

                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(
                    content: Text("Plant deleted successfully"),
                  ),
                );
              },

              child: const Text("Delete"),
            )
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {

    return Scaffold(

      appBar: AppBar(
        title: const Text("Delete Plant"),
        centerTitle: true,
      ),

      body: plants.isEmpty
          ? const Center(
        child: Text(
          "No plants available",
          style: TextStyle(fontSize: 18),
        ),
      )

          : ListView.builder(

        padding: const EdgeInsets.all(20),

        itemCount: plants.length,

        itemBuilder: (context, index) {

          return Card(
            elevation: 5,

            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(15),
            ),

            child: ListTile(

              leading: const Icon(
                Icons.eco,
                color: Colors.green,
              ),

              title: Text(plants[index]["name"]),

              trailing: IconButton(

                icon: const Icon(
                  Icons.delete,
                  color: Colors.red,
                ),

                onPressed: () {
                  deletePlant(index);
                },
              ),
            ),
          );
        },
      ),
    );
  }
}