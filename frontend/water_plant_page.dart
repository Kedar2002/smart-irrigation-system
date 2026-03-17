import 'package:flutter/material.dart';

class WaterPlantPage extends StatefulWidget {
  const WaterPlantPage({super.key});

  @override
  State<WaterPlantPage> createState() => _WaterPlantPageState();
}

class _WaterPlantPageState extends State<WaterPlantPage>
    with SingleTickerProviderStateMixin {

  late TabController _tabController;

  String selectedPlant = "Rose";
  final TextEditingController waterController = TextEditingController();

  DateTime? selectedDate;
  TimeOfDay? selectedTime;

  /// DEMO SENSOR DATA
  List<Map<String, dynamic>> sensorData = [
    {
      "plant": "Rose",
      "temp": "28°C",
      "humidity": "65%",
      "soil": "40%",
      "height": "25 cm"
    },
    {
      "plant": "Tulsi",
      "temp": "27°C",
      "humidity": "70%",
      "soil": "55%",
      "height": "18 cm"
    },
    {
      "plant": "Money Plant",
      "temp": "29°C",
      "humidity": "60%",
      "soil": "35%",
      "height": "30 cm"
    },
  ];

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
  }

  /// DATE PICKER
  Future<void> pickDate() async {
    DateTime? date = await showDatePicker(
      context: context,
      initialDate: DateTime.now(),
      firstDate: DateTime.now(),
      lastDate: DateTime(2100),
    );

    if (date != null) {
      setState(() {
        selectedDate = date;
      });
    }
  }

  /// TIME PICKER
  Future<void> pickTime() async {
    TimeOfDay? time = await showTimePicker(
      context: context,
      initialTime: TimeOfDay.now(),
    );

    if (time != null) {
      setState(() {
        selectedTime = time;
      });
    }
  }

  @override
  Widget build(BuildContext context) {

    return Scaffold(

      appBar: AppBar(
        title: const Text("Water Plants"),
        centerTitle: true,
      ),

      body: Column(
        children: [

          /// SENSOR DASHBOARD
          Container(
            padding: const EdgeInsets.all(15),
            color: Colors.green.shade50,

            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [

                const Text(
                  "Current Sensor Readings",
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),

                const SizedBox(height: 10),

                SizedBox(
                  height: 140, // FIXED HEIGHT TO PREVENT OVERFLOW

                  child: ListView.builder(
                    scrollDirection: Axis.horizontal,
                    itemCount: sensorData.length,

                    itemBuilder: (context, index) {

                      final plant = sensorData[index];

                      return Container(
                        width: 170,
                        margin: const EdgeInsets.only(right: 12),
                        padding: const EdgeInsets.all(12),

                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(15),
                          boxShadow: const [
                            BoxShadow(
                              color: Colors.black12,
                              blurRadius: 5,
                            )
                          ],
                        ),

                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          mainAxisSize: MainAxisSize.min,

                          children: [

                            Text(
                              plant["plant"],
                              style: const TextStyle(
                                fontWeight: FontWeight.bold,
                                fontSize: 16,
                              ),
                            ),

                            const SizedBox(height: 6),

                            Text("🌡 Temp: ${plant["temp"]}"),
                            Text("💧 Soil: ${plant["soil"]}"),
                            Text("💨 Humidity: ${plant["humidity"]}"),
                            Text("📏 Height: ${plant["height"]}"),
                          ],
                        ),
                      );
                    },
                  ),
                ),
              ],
            ),
          ),

          /// TAB BAR
          TabBar(
            controller: _tabController,
            labelColor: Colors.green,
            tabs: const [
              Tab(text: "Irrigate Now"),
              Tab(text: "Schedule Irrigation"),
            ],
          ),

          /// TAB CONTENT
          Expanded(
            child: TabBarView(
              controller: _tabController,

              children: [

                /// IRRIGATE NOW TAB
                SingleChildScrollView(
                  padding: const EdgeInsets.all(20),

                  child: Column(
                    children: [

                      DropdownButtonFormField(
                        value: selectedPlant,

                        decoration: const InputDecoration(
                          labelText: "Select Plant",
                        ),

                        items: const [
                          DropdownMenuItem(value: "Rose", child: Text("Rose")),
                          DropdownMenuItem(value: "Tulsi", child: Text("Tulsi")),
                          DropdownMenuItem(value: "Money Plant", child: Text("Money Plant")),
                        ],

                        onChanged: (value) {
                          setState(() {
                            selectedPlant = value.toString();
                          });
                        },
                      ),

                      const SizedBox(height: 20),

                      TextField(
                        controller: waterController,
                        keyboardType: TextInputType.number,

                        decoration: const InputDecoration(
                          labelText: "Water Amount (ml)",
                        ),
                      ),

                      const SizedBox(height: 30),

                      SizedBox(
                        width: double.infinity,
                        height: 50,

                        child: ElevatedButton(
                          onPressed: () {

                            ScaffoldMessenger.of(context).showSnackBar(
                              const SnackBar(
                                content: Text("Irrigation Started 💧"),
                              ),
                            );

                          },

                          child: const Text("START IRRIGATION"),
                        ),
                      )
                    ],
                  ),
                ),

                /// SCHEDULE IRRIGATION TAB
                SingleChildScrollView(
                  padding: const EdgeInsets.all(20),

                  child: Column(
                    children: [

                      DropdownButtonFormField(
                        value: selectedPlant,

                        decoration: const InputDecoration(
                          labelText: "Select Plant",
                        ),

                        items: const [
                          DropdownMenuItem(value: "Rose", child: Text("Rose")),
                          DropdownMenuItem(value: "Tulsi", child: Text("Tulsi")),
                          DropdownMenuItem(value: "Money Plant", child: Text("Money Plant")),
                        ],

                        onChanged: (value) {
                          setState(() {
                            selectedPlant = value.toString();
                          });
                        },
                      ),

                      const SizedBox(height: 20),

                      ListTile(
                        title: Text(
                          selectedDate == null
                              ? "Select Date"
                              : selectedDate.toString().split(" ")[0],
                        ),
                        trailing: const Icon(Icons.calendar_today),
                        onTap: pickDate,
                      ),

                      ListTile(
                        title: Text(
                          selectedTime == null
                              ? "Select Time"
                              : selectedTime!.format(context),
                        ),
                        trailing: const Icon(Icons.access_time),
                        onTap: pickTime,
                      ),

                      const SizedBox(height: 30),

                      SizedBox(
                        width: double.infinity,
                        height: 50,

                        child: ElevatedButton(
                          onPressed: () {

                            ScaffoldMessenger.of(context).showSnackBar(
                              const SnackBar(
                                content: Text("Irrigation Scheduled ⏰"),
                              ),
                            );

                          },

                          child: const Text("SCHEDULE"),
                        ),
                      )
                    ],
                  ),
                )
              ],
            ),
          ),
        ],
      ),
    );
  }
}