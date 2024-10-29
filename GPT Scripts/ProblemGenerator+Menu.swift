//
//  ProblemGenerator+Menu.swift
//  GPT Scripts
//
//  Created by TaeVon Lewis on 10/29/24.
//

import Foundation

extension ProblemGenerator {
    // MARK: - Main Menu
    func mainMenu() {
        while true {
            print("\nMain Menu")
            print("1. Generate New Problem")
            print("2. Review Past Problems")
            print("3. Continue Multi-Part Problem")
            print("4. Evaluate Solution")
            print("5. Exit")
            print("Choose an option: ", terminator: "")
            guard let choice = readLine()?.trimmingCharacters(in: .whitespacesAndNewlines) else {
                print("Invalid input.")
                continue
            }
            switch choice {
            case "1":
                generateNewProblem()
            case "2":
                reviewProblems()
            case "3":
                multiPartMenu()
            case "4":
                evaluateSolution()
            case "5":
                print("Exiting. Good luck with your preparation!")
                exit(0)
            default:
                print("Invalid selection. Please try again.")
            }
        }
    }

    func multiPartMenu() {
        while true {
            print("\nMulti-Part Problem Menu")
            print("1. Generate Next Part")
            print("2. Return to Main Menu")
            print("Choose an option: ", terminator: "")
            guard let choice = readLine()?.trimmingCharacters(in: .whitespacesAndNewlines) else {
                print("Invalid input.")
                continue
            }
            if choice == "1" {
                generateNextPart()
            } else if choice == "2" {
                break
            } else {
                print("Invalid selection. Please try again.")
            }
        }
    }

    // MARK: - Problem Review
    func reviewProblems() {
        if history.isEmpty {
            print("No problems to review.")
            return
        }
        for (idx, entry) in history.enumerated() {
            print("\nProblem \(idx + 1) (\(entry["difficulty"] ?? "") - \(entry["part_type"] ?? "") - \(entry["style"] ?? "")):")
            print("Timestamp: \(entry["timestamp"] ?? "")")
            print("Filename: \(entry["filename"] ?? "")")
            print("Problem:\n\(entry["problem"] ?? "")\n")
        }
    }
}
