#include <iostream>
#include <vector>
#include <map>
#include <string>
#include <algorithm>

using namespace std;

void setup() {
  // put your setup code here, to run once:
// Define a struct to hold the shirt details
struct Shirt {
    string name;
    string ID;
    vector<string> details;

    // Function to print shirt details
    void print() const {
        cout << "Shirt ID: " << ID << endl;
        cout << "Shirt Name: " << name << endl;
        cout << "Tags: " << endl;
        for (const auto& detail : details) {
            cout << "- " << detail << endl;
        }
        cout << endl;
    }

    // Function to check if any detail contains the search term
    bool contains(const string& term) const {
        if (name.find(term) != string::npos) {
            return true;
        }
        for (const auto& detail : details) {
            if (detail.find(term) != string::npos) {
                return true;
            }
        }
        return false;
    }
};

// Function to input shirt details from the user
Shirt inputShirt() {
    Shirt shirt;
    string detail;

    cout << "Enter shirt ID: ";
    getline(cin, shirt.ID);

    cout << "Enter shirt name: ";
    getline(cin, shirt.name);

    while (true) {
        cout << "Enter detail (or type 'done' to finish): ";
        getline(cin, detail);
        if (detail == "done") {
            break;
        }
        shirt.details.push_back(detail);
    }

    return shirt;
}

// Remove clothing from closet
void removeClothes(vector<Shirt>& closet){
    string ChosenID;
    cout << "Enter the shirt ID that you want to remove" << endl;
    getline(cin, ChosenID);
    
    auto it = find_if(closet.begin(), closet.end(), [&](const Shirt& shirt){
        return shirt.ID == ChosenID;
    });

    if (it != closet.end()){
        closet.erase(it);
        cout << "Shirt removed successfully." << endl;
    }else{
        cout << "There are no shirts with the ID of " << ChosenID << endl;
    }
}
// Function to print all shirts in the closet
void printCloset(const vector<Shirt>& closet) {
    cout << "Closet contents:" << endl;
    for (size_t i = 0; i < closet.size(); ++i) {
        cout << "Shirt " << i + 1 << ":" << endl;
        closet[i].print();
    }
}

// Search Function
void SearchClothes(const vector<Shirt>& closet){
    // Prompt user to enter a search term
    string searchTerm;
    cout << "Enter a detail to search for: ";
    getline(cin, searchTerm);
    cout << "Current Filters: " << endl;
    // Search and print shirts that contain the search term
    bool found = false;
    for (const auto& shirt : closet) {
        if (shirt.contains(searchTerm)) {
            shirt.print();
            found = true;
        }
    }

    if (!found) {
        cout << "No shirts found with the detail: " << searchTerm << endl;
    }
}

void loop() {
  // put your main code here, to run repeatedly:
   // Create a vector to store the shirts
    vector<Shirt> closet;
    
    string command;
    
    cout << "Welcome to the Closet Manager" << endl;

    while (true) {
        cout << "Please choose an option" << endl;
        cout << "1. Add clothing" << endl;
        cout << "2. Remove clothing" << endl;
        cout << "3. View current closet" << endl;
        cout << "4. Search for specific clothing" << endl;
        cout << "5. Exit" << endl;
        cout << "Select options from 1 to 5: ";
        getline(cin, command);
        
        if (command == "done") {
            break;
        } else if (command == "1") {
            closet.push_back(inputShirt());
        } else if (command == "2") {
            removeClothes(closet);    
        } else if (command == "3") {
            printCloset(closet);
        } else if (command == "4"){
            SearchClothes(closet);
        } else {
            cout << "Invalid command. Select a valid number." << endl;
        }
    }

    

    return 0;

}
