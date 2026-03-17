import 'package:flutter/material.dart';
import 'add_plant_page.dart';
import 'delete_plant_page.dart';
import 'water_plant_page.dart';
import 'plant_details_page.dart';
import 'profile_page.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [
              Color(0xff4CAF50),
              Color(0xffA8E063),
            ],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),

        child: SafeArea(
          child: Column(
            children: [

              /// HEADER
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),

                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [

                    Row(
                      children: [

                        /// LOGO
                        Image.asset(
                          "assets/logo1.png",
                          height: 40,
                        ),

                        const SizedBox(width: 10),

                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: const [

                            Text(
                              "PlantBuddy",
                              style: TextStyle(
                                fontSize: 26,
                                fontWeight: FontWeight.bold,
                                color: Colors.white,
                              ),
                            ),

                            Text(
                              "Welcome back 🌿",
                              style: TextStyle(
                                color: Colors.white70,
                                fontSize: 14,
                              ),
                            )
                          ],
                        ),
                      ],
                    ),

                    CircleAvatar(
                      backgroundColor: Colors.white,
                      child: IconButton(
                        icon: const Icon(Icons.menu, color: Colors.green),

                        onPressed: () {

                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) => const ProfilePage(),
                            ),
                          );

                        },
                      ),
                    )
                  ],
                ),
              ),

              const SizedBox(height: 20),

              /// PLANT IMAGE (BIGGER)
              Image.asset(
                "assets/plants.png",
                height: 250,
              ),

              const SizedBox(height: 20),

              /// DASHBOARD CONTAINER
              Expanded(
                child: Container(
                  padding: const EdgeInsets.all(25),

                  decoration: const BoxDecoration(
                    color: Color(0xffF6F6F6),
                    borderRadius: BorderRadius.only(
                      topLeft: Radius.circular(35),
                      topRight: Radius.circular(35),
                    ),
                  ),

                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [

                      const Text(
                        "Your Garden",
                        style: TextStyle(
                          fontSize: 22,
                          fontWeight: FontWeight.bold,
                        ),
                      ),

                      const SizedBox(height: 20),

                      Expanded(
                        child: GridView.count(
                          crossAxisCount: 2,
                          crossAxisSpacing: 20,
                          mainAxisSpacing: 20,

                          children: [

                            dashboardCard(
                              context,
                              "Add Plant",
                              Icons.add,
                              const AddPlantPage(),
                            ),

                            dashboardCard(
                              context,
                              "Delete Plant",
                              Icons.delete_outline,
                              const DeletePlantPage(),
                            ),

                            dashboardCard(
                              context,
                              "Water Plants",
                              Icons.water_drop_outlined,
                              const WaterPlantPage(),
                            ),

                            dashboardCard(
                              context,
                              "Plant Details",
                              Icons.eco_outlined,
                              const PlantDetailsPage(),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  /// DASHBOARD CARD
  Widget dashboardCard(
      BuildContext context,
      String title,
      IconData icon,
      Widget page,
      ) {

    return InkWell(

      borderRadius: BorderRadius.circular(22),

      onTap: () {

        Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => page),
        );

      },

      child: Ink(

        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(22),

          boxShadow: const [
            BoxShadow(
              color: Colors.black12,
              blurRadius: 15,
              offset: Offset(0,6),
            )
          ],
        ),

        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [

            /// ICON CIRCLE
            Container(
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: Colors.green.withOpacity(0.15),
                shape: BoxShape.circle,
              ),
              child: Icon(
                icon,
                size: 32,
                color: Colors.green,
              ),
            ),

            const SizedBox(height: 12),

            Text(
              title,
              textAlign: TextAlign.center,
              style: const TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.w600,
              ),
            )
          ],
        ),
      ),
    );
  }
}