Mock:/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany.cosc005w_mock_planeapp;

import java.util.Scanner;
import java.io.File;
import java.io.FileWriter;
import java.util.InputMismatchException;

public class ExamPrep3 {

    // Global variables
    private static int[][] theaterSeats = null; // Changed from planeSeats to theaterSeats
    private static int[] pricePerRow = null;
    private static Person[] persons = new Person[100]; // Array to store Person objects
    private static int personCount = 0; // Counter for persons

    public static void main(String[] args) {
        System.out.println("Welcome to the Theater!");
        initialiseRows();
        runMenu();
    }

    public static void initialiseRows() {
        theaterSeats = new int[5][]; // total rows - modified to 5 rows
        theaterSeats[0] = new int[16]; // Row 1
        theaterSeats[1] = new int[22]; // Row 2
        theaterSeats[2] = new int[22]; // Row 3
        theaterSeats[3] = new int[16]; // Row 4
        theaterSeats[4] = new int[20]; // New Row 5
        pricePerRow = new int[5];
        pricePerRow[0] = 50; // Price for Row 1
        pricePerRow[1] = 80; // Price for Row 2
        pricePerRow[2] = 80; // Price for Row 3
        pricePerRow[3] = 50; // Price for Row 4
        pricePerRow[4] = 60; // Price for Row 5
    }

    public static void runMenu() {
        int option;
        boolean cont = true;

        while (cont) {
            option = getOption();
            switch (option) {
                case 0:
                    cont = false;
                    break;
                case 1:
                    buyTicket();
                    break;
                case 2:
                    showSeatingArea();
                    break;
                case 3:
                    searchPerson();
                    break;
                case 4:
                    saveToFile();
                    break;
                default:
                    System.out.println("Option not available. Please select a valid option: ");
            }
        }
    }

    private static int getOption() {
        Scanner input = new Scanner(System.in);
        boolean valid = false;
        int option = -1;
        do {
            System.out.println();
            System.out.println("+---------------------------------------------+");
            System.out.println("|                MAIN MENU                    |");
            System.out.println("+---------------------------------------------+");
            System.out.println("|  1) Buy a theater ticket                    |");
            System.out.println("|  2) Show seating area and available seats   |");
            System.out.println("|  3) Search for persons                      |");
            System.out.println("|  4) Save to File                            |");
            System.out.println("|  0) Quit                                    |");
            System.out.println("+---------------------------------------------+");
            System.out.print("Please select an option: ");
            try {
                option = input.nextInt();
                valid = true;
            } catch (Exception e) {
                System.out.println("This option is not valid.");
                input.next(); // Clear invalid input
            }
        } while (!valid);
        return option;
    }

    private static void buyTicket() {
        Scanner input = new Scanner(System.in);
        String email = "";
        String surname = "";
        boolean emailValid = false;

        // Validate email input
        do {
            System.out.print("Enter your email: ");
            email = input.nextLine();
            if (email.contains("@") && email.contains(".")) {
                emailValid = true;
            } else {
                System.out.println("Invalid email");
            }
        } while (!emailValid);

        // Get surname from user
        System.out.print("Enter your surname: ");
        surname = input.nextLine();

        int row = -1;
        boolean validRow = false;

        // Validate row input
        do {
            try {
                System.out.print("Enter row number (1-5): ");
                row = input.nextInt() - 1; // Adjust for 0-based index
                if (row < 0 || row >= theaterSeats.length) {
                    System.out.println("Row number must be between 1 and 5!");
                } else {
                    validRow = true;
                }
            } catch (InputMismatchException e) {
                System.out.println("Invalid input. Please enter a number.");
                input.next(); // Clear invalid input
            }
        } while (!validRow);

        int seat = -1;
        boolean validSeat = false;

        // Validate seat input
        do {
            try {
                System.out.print("Enter seat number: ");
                seat = input.nextInt() - 1; // Adjust for 0-based index
                if (seat < 0 || seat >= theaterSeats[row].length) {
                    System.out.println("Seat number must be valid for the selected row!");
                } else if (theaterSeats[row][seat] == 1) {
                    System.out.println("Seat already taken. Please choose another seat.");
                } else {
                    validSeat = true;
                }
            } catch (InputMismatchException e) {
                System.out.println("Invalid input. Please enter a number.");
                input.next(); // Clear invalid input
            }
        } while (!validSeat);

        // Mark the seat as taken
        theaterSeats[row][seat] = 1;

        // Create a new Person object and add it to the array
        Person newPerson = new Person(email, surname, row + 1, seat + 1);
        persons[personCount++] = newPerson;

        System.out.println("Ticket purchased successfully!");
    }

    private static void showSeatingArea() {
        System.out.println("Seating Area:");
        for (int i = 0; i < theaterSeats.length; i++) {
            System.out.print("Row " + (i + 1) + ": ");
            for (int j = 0; j < theaterSeats[i].length; j++) {
                if (theaterSeats[i][j] == 1) {
                    System.out.print("[X] "); // Seat taken
                } else {
                    System.out.print("[O] "); // Seat available
                }
            }
            System.out.println();
        }
    }

    private static void searchPerson() {
        Scanner input = new Scanner(System.in);
        System.out.print("Enter surname to search: ");
        String surname = input.nextLine();
        boolean found = false;

        for (int i = 0; i < personCount; i++) {
            if (persons[i] != null && persons[i].getSurname().equalsIgnoreCase(surname)) {
                persons[i].printInfo();
                found = true;
            }
        }

        if (!found) {
            System.out.println("No persons found with the surname: " + surname);
        }
    }

    private static void saveToFile() {
        try {
            File file = new File("tickets.txt");
            if (!file.exists()) {
                file.createNewFile();
            } // Create file if it doesn't exist
            FileWriter writer = new FileWriter("tickets.txt");
            for (int i = 0; i < personCount; i++) {
                if (persons[i] != null) {
                    writer.write("Email: " + persons[i].getEmail() + ", Surname: " + persons[i].getSurname() + ", Row: " + persons[i].getRow() + ", Seat: " + persons[i].getSeat() + "\n");
                }
            }
            writer.close();
            System.out.println("Data saved successfully!");
        } catch (Exception e) {
            System.out.println("Error saving data: " + e.getMessage());
        }
    }
}

class Person {
    private String email;
    private String surname; // Added surname attribute
    private int row;
    private int seat;

    public Person(String email, String surname, int row, int seat) {
        this.email = email;
        this.surname = surname; // Initialize surname
        this.row = row;
        this.seat = seat;
    }

    // Setters
    public void setEmail(String email) {
        this.email = email;
    }

    public void setSurname(String surname) {
        this.surname = surname; // Setter for surname
    }

    public void setRow(int row) {
        this.row = row;
    }

    public void setSeat(int seat) {
        this.seat = seat;
    }

    // Getters
    public String getEmail() {
        return email;
    }

    public String getSurname() {
        return surname; // Getter for surname
    }

    public int getRow() {
        return row;
    }

    public int getSeat() {
        return seat;
    }

    public void printInfo() {
        System.out.println("Email: " + email + ", Surname: " + surname + ", Row: " + row + ", Seat: " + seat);
    }
}
