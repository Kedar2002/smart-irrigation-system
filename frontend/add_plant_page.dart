import 'package:flutter/material.dart';

class AddPlantPage extends StatefulWidget {
  const AddPlantPage({super.key});

  @override
  State<AddPlantPage> createState() => _AddPlantPageState();
}

class _AddPlantPageState extends State<AddPlantPage> {

  final _formKey = GlobalKey<FormState>();

  final TextEditingController plantNameController = TextEditingController();
  final TextEditingController plantAgeController = TextEditingController();
  final TextEditingController plantHeightController = TextEditingController();
  final TextEditingController notesController = TextEditingController();

  String? plantType;
  String? potSize;
  String? planterType;

  void savePlant() {

    if (_formKey.currentState!.validate()) {

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text("Plant added successfully 🌱"),
        ),
      );

      Navigator.pop(context);
    }
  }

  @override
  Widget build(BuildContext context) {

    return Scaffold(

      appBar: AppBar(
        title: const Text("Add Plant"),
        centerTitle: true,
      ),

      body: Container(

        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [
              Color(0xff6dbf43),
              Color(0xffa8e063),
            ],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
        ),

        child: SingleChildScrollView(
          padding: const EdgeInsets.all(20),

          child: Card(
            elevation: 10,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(20),
            ),

            child: Padding(
              padding: const EdgeInsets.all(20),

              child: Form(
                key: _formKey,

                child: Column(
                  children: [

                    Image.asset(
                      "assets/rose.png",
                      height: 200,
                    ),

                    const SizedBox(height: 20),
                    /// PLANT NAME
                    TextFormField(
                      controller: plantNameController,
                      decoration: const InputDecoration(
                        labelText: "Plant Name",
                        prefixIcon: Icon(Icons.eco),
                      ),

                      validator: (value) {
                        if (value == null || value.isEmpty) {
                          return "Plant name is required";
                        }
                        return null;
                      },
                    ),

                    const SizedBox(height: 15),

                    /// PLANT TYPE
                    DropdownButtonFormField(
                      decoration: const InputDecoration(
                        labelText: "Plant Type",
                        prefixIcon: Icon(Icons.local_florist),
                      ),

                      value: plantType,

                      items: const [
                        DropdownMenuItem(value: "Rose", child: Text("Rose")),
                        DropdownMenuItem(value: "Tulsi", child: Text("Tulsi")),
                      ],

                      onChanged: (value) {
                        setState(() {
                          plantType = value.toString();
                        });
                      },

                      validator: (value) {
                        if (value == null) {
                          return "Please select plant type";
                        }
                        return null;
                      },
                    ),

                    const SizedBox(height: 15),

                    /// PLANT AGE
                    TextFormField(
                      controller: plantAgeController,
                      keyboardType: TextInputType.number,

                      decoration: const InputDecoration(
                        labelText: "Plant Age (days)",
                        prefixIcon: Icon(Icons.calendar_today),
                      ),

                      validator: (value) {

                        if (value == null || value.isEmpty) {
                          return "Plant age is required";
                        }

                        if (int.tryParse(value) == null) {
                          return "Enter a valid number";
                        }

                        return null;
                      },
                    ),

                    const SizedBox(height: 15),

                    /// PLANT HEIGHT
                    TextFormField(
                      controller: plantHeightController,
                      keyboardType: TextInputType.number,

                      decoration: const InputDecoration(
                        labelText: "Plant Height (cm)",
                        prefixIcon: Icon(Icons.height),
                      ),

                      validator: (value) {

                        if (value == null || value.isEmpty) {
                          return "Plant height is required";
                        }

                        if (double.tryParse(value) == null) {
                          return "Enter valid height";
                        }

                        return null;
                      },
                    ),

                    const SizedBox(height: 15),

                    /// POT SIZE
                    DropdownButtonFormField(
                      decoration: const InputDecoration(
                        labelText: "Pot Size",
                        prefixIcon: Icon(Icons.crop_square),
                      ),

                      value: potSize,

                      items: const [
                        DropdownMenuItem(value: "1L", child: Text("1L")),
                        DropdownMenuItem(value: "2L", child: Text("2L")),
                        DropdownMenuItem(value: "5L", child: Text("5L")),
                        DropdownMenuItem(value: "10L", child: Text("10L")),
                      ],

                      onChanged: (value) {
                        setState(() {
                          potSize = value.toString();
                        });
                      },

                      validator: (value) {
                        if (value == null) {
                          return "Please select pot size";
                        }
                        return null;
                      },
                    ),

                    const SizedBox(height: 15),

                    /// PLANTER TYPE
                    DropdownButtonFormField(
                      decoration: const InputDecoration(
                        labelText: "Planter Type",
                        prefixIcon: Icon(Icons.category),
                      ),

                      value: planterType,

                      items: const [
                        DropdownMenuItem(value: "Plastic", child: Text("Plastic")),
                        DropdownMenuItem(value: "Clay", child: Text("Clay")),
                        DropdownMenuItem(value: "Ceramic", child: Text("Ceramic")),
                        DropdownMenuItem(value: "Grow Bag", child: Text("Grow Bag")),
                      ],

                      onChanged: (value) {
                        setState(() {
                          planterType = value.toString();
                        });
                      },

                      validator: (value) {
                        if (value == null) {
                          return "Please select planter type";
                        }
                        return null;
                      },
                    ),

                    const SizedBox(height: 15),

                    /// NOTES
                    TextField(
                      controller: notesController,
                      decoration: const InputDecoration(
                        labelText: "Notes (Optional)",
                        prefixIcon: Icon(Icons.note),
                      ),
                    ),

                    const SizedBox(height: 25),

                    /// SAVE BUTTON
                    SizedBox(
                      width: double.infinity,
                      height: 50,

                      child: ElevatedButton(
                        onPressed: savePlant,
                        child: const Text(
                          "SAVE PLANT",
                          style: TextStyle(fontSize: 16),
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
    );
  }
}