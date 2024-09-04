#include <iostream>
#include <vector>
#include <map>
#include <string>
#include <algorithm>
#include <fstream>

using namespace std;

// Define a struct to hold the clothing details
struct Clothing {
    string name;
    string ID;
    vector<string> details;

    // Function to print clothing details
    void print() const {
        cout << "Clothing ID: " << ID << endl;
        cout << "Clothing Name: " << name << endl;
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

// Structure to input clothing details from the user
Clothing inputClothing() {
    Clothing Clothing;
    string detail;

    cout << "Enter Clothing ID: ";
    getline(cin, Clothing.ID);

    cout << "Enter Clothing Name: ";
    getline(cin, Clothing.name);
    //Adds details to the clothing
    while (true) {
        cout << "Enter Detail (or type 'done' to finish): ";
        getline(cin, detail);
        if (detail == "done") {
            break;
        }
        Clothing.details.push_back(detail);
    }

    return Clothing;
}

// Remove clothing from closet
void removeClothes(vector<Clothing>& closet){
    string ChosenID;
    cout << "Enter the Clothing ID that you want to remove" << endl;
    getline(cin, ChosenID);
    
    auto it = find_if(closet.begin(), closet.end(), [&](const Clothing& Clothing){
        return Clothing.ID ==
         ChosenID;
    });

    if (it != closet.end()){
        closet.erase(it);
        cout << "Clothing removed successfully." << endl;
    }else{
        cout << "There are no Clothings with the ID of " << ChosenID << endl;
    }
}
// Function to print all clothings in the closet
void printCloset(const vector<Clothing>& closet) {
    cout << "Closet contents:" << endl;
    for (size_t i = 0; i < closet.size(); ++i) {
        cout << "Clothing " << i + 1 << ":" << endl;
        closet[i].print();
    }
}

// Function to update clothing
void updateClothes(vector<Clothing>& closet){
    string ChosenID;
    string choice; 
    string detail_add;
    string detail_remove;
    cout << "Enter the clothing ID that you want to update" << endl;
    getline(cin, ChosenID);

    auto it = find_if(closet.begin(), closet.end(), [&](const Clothing& Clothing){
        return Clothing.ID == ChosenID;
    });
    //Checks to see if the inputted ID matches with a stored ID
    if (it != closet.end()){
        cout << "Clothing ID found" << endl;
        while(true){
        it->print();
        cout << "Do you want to 'add' or 'remove' details(Type 'exit' to exit)?" << endl;
        getline(cin, choice);
        //Adds additional details
        if(choice == "add"){
            while (true) {
            cout << "Enter detail (or type 'done' to finish): ";
            getline(cin, detail_add);
            if (detail_add == "done") {
                break;
                }
            it->details.push_back(detail_add);
            }
        //Removes existing details
        }else if (choice == "remove"){
            while (true) {
            cout << "Enter existing detail to remove (or type 'done' to finish): ";
            getline(cin, detail_remove);
            if (detail_remove == "done") {
                break;
                }
            
            auto detailIt = find(it->details.begin(), it->details.end(), detail_remove);
            if (detailIt != it->details.end()){
                it->details.erase(detailIt);
                cout << "Detail removed successfully. " << endl;
            } else{
                cout << "Detail not found." << endl;
                }
            }
        }else if (choice == "exit"){
            break;
        }else{
            cout << "Invalid choice. Please type 'add' or 'remove' " << endl;
        }
    }
    }else{
        cout << "Clothing ID not found." << endl;
    }
 }
// Search Function
void SearchClothes(const vector<Clothing>& closet){
    // Prompt user to enter a search term
    string searchTerm;
    cout << "Enter a detail to search for: ";
    getline(cin, searchTerm);
    cout << "Current Filters: " << searchTerm << endl;
    // Search and print clothing that contain the search term
    bool found = false;
    for (const auto& Clothing : closet) {
        if (Clothing.contains(searchTerm)) {
            Clothing.print();
            found = true;
        }
    }

    if (!found) {
        cout << "No clothings found with the detail: " << searchTerm << endl;
    }
}

// Function to save the closet to a file
void saveCloset(const vector<Clothing>& closet, const string& filename) {
    ofstream outFile(filename);

    if (!outFile) {
        cout << "Error opening text file!" << endl;
        return;
    }

    for (const auto& clothes : closet) {
        outFile << "Clothing ID: " << clothes.ID << endl;
        outFile << "Clothing Name: " << clothes.name << endl;
        for (const auto& detail : clothes.details) {
            outFile << "- " << detail << endl;
        }
    }

    outFile.close();
    cout << "Closet saved to " << filename << endl;
}

// Function to load the closet from a file in the same format as it was saved
void loadCloset(vector<Clothing>& closet, const string& filename) {
    ifstream inFile(filename);

    if (!inFile) {
        cout << "Error opening file for loading!" << endl;
        return;
    }

    closet.clear();
    Clothing clothes;
    string line;

    while (getline(inFile, line)) {
        if (line.find("Clothing ID:") != string::npos) {
            if (!clothes.name.empty()) {
                closet.push_back(clothes);  // Save the previous clothing item before starting a new one
            }

            clothes = Clothing();  // Reset the clothing object for the new item
            clothes.ID = line.substr(line.find(":") + 2);
        }
        else if (line.find("Clothing Name:") != string::npos) {
            clothes.name = line.substr(line.find(":") + 2);
        }
        else if (line.find("- ") == 0) {
            clothes.details.push_back(line.substr(2));  // Add the detail to the list
        }
    }

    if (!clothes.name.empty()) {
        closet.push_back(clothes);  // Save the last clothing item
    }

    inFile.close();
    cout << "Closet loaded from " << filename << endl;
}

int main() {
    // Create a vector to store the Clothings
    vector<Clothing> closet;
    
    string command;
    //Menu for Closet Manager
    cout << "Welcome to the Closet Manager" << endl;

    while (true) {
        cout << "Please choose an option" << endl;
        cout << "1. Add clothing" << endl;
        cout << "2. Remove clothing" << endl;
        cout << "3. View current closet" << endl;
        cout << "4. Update current clothing" << endl;
        cout << "5. Search for specific clothing" << endl;
        cout << "6. Save closet information to a text file" << endl;
        cout << "7. Load closet information from a text file" << endl;
        cout << "8. Exit" << endl;
        cout << "Select options from 1 to 8: ";
        getline(cin, command);
        
        if (command == "done") {
            break;
        } else if (command == "1") {
            closet.push_back(inputClothing());
        } else if (command == "2") {
            removeClothes(closet);    
        } else if (command == "3") {
            printCloset(closet);
        } else if (command == "4") {
            updateClothes(closet);    
        } else if (command == "5"){
            SearchClothes(closet);
        } else if (command == "6"){
            string filename;
            cout << "Enter file name to save to: ";
            getline(cin, filename);
            saveCloset(closet, filename);
        }else if (command == "7"){
            string filename;
            cout << "Enter file name to load from: ";
            getline(cin, filename);
            loadCloset(closet, filename);
        }else if (command == "8"){
            break;
        } else {
            cout << "Invalid command. Select a valid number." << endl;
        }
    }
    return 0;
}
