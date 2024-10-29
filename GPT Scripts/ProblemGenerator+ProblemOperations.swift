//
//  ProblemGenerator+ProblemOperations.swift
//  GPT Scripts
//
//  Created by TaeVon Lewis on 10/29/24.
//

import Foundation

extension ProblemGenerator {
    // MARK: - Generate New Problem (Full Implementation)
    func generateNewProblem() {
        print("Do you want to select a difficulty level? (y/n): ", terminator: "")
        guard let manualChoice = readLine()?.trimmingCharacters(in: .whitespacesAndNewlines).lowercased() else {
            print("Invalid input.")
            return
        }
        if manualChoice == "y" {
            print("Choose difficulty (Easy, Medium, Hard): ", terminator: "")
            guard let difficulty = readLine()?.trimmingCharacters(in: .whitespacesAndNewlines).capitalized,
                  difficultyLevels.contains(difficulty) else {
                print("Invalid difficulty level selected. Defaulting to Easy.")
                currentDifficulty = "Easy"
                return
            }
            currentDifficulty = difficulty
        } else {
            var problemCounts = [String: Int]()
            for level in difficultyLevels {
                problemCounts[level] = 0
            }
            for entry in history {
                if let difficulty = entry["difficulty"] as? String {
                    problemCounts[difficulty, default: 0] += 1
                }
            }
            if (problemCounts[currentDifficulty] ?? 0) >= 5 {
                if let currentIndex = difficultyLevels.firstIndex(of: currentDifficulty), currentIndex + 1 < difficultyLevels.count {
                    currentDifficulty = difficultyLevels[currentIndex + 1]
                    print("Moving to \(currentDifficulty) problems.")
                }
            }
        }

        print("Select problem type (single-part, multi-part): ", terminator: "")
        guard let partType = readLine()?.trimmingCharacters(in: .whitespacesAndNewlines).lowercased(),
              ["single-part", "multi-part"].contains(partType) else {
            print("Invalid selection. Please try again.")
            return
        }

        print("Select style (leetcode, real-world): ", terminator: "")
        guard let style = readLine()?.trimmingCharacters(in: .whitespacesAndNewlines).lowercased(),
              ["leetcode", "real-world"].contains(style) else {
            print("Invalid selection. Please try again.")
            return
        }

        let part = (partType == "single-part") ? "single" : "multi"
        let partNumber = 1

        let prompt = generateProblemPrompt(part: part, style: style, difficulty: currentDifficulty, partNumber: partNumber)
        if let problem = callOpenAIAPI(prompt: prompt) {
            let cleanProblem = problem

            print("\nGenerated Problem (\(currentDifficulty)):\n\(cleanProblem)\n")

            let title = extractProblemTitle(problemContent: cleanProblem)
            let formattedTitle = formatTitleForFilename(title: title)
            let timestamp = getCurrentTimestamp()
            let filename = "\(formattedTitle)_\(timestamp).md"

            saveProblemToFile(problem: cleanProblem, filename: filename)

            let problemEntry: [String: Any] = [
                "problem": cleanProblem,
                "difficulty": currentDifficulty,
                "part_type": partType,
                "style": style,
                "timestamp": timestamp,
                "filename": filename
            ]
            addProblemToHistory(problemEntry: problemEntry)

            if part == "multi" {
                progress = [
                    "current_part": partNumber,
                    "part_type": partType,
                    "style": style,
                    "difficulty": currentDifficulty,
                    "problem_history": [problemEntry]
                ]
                saveProgress()
                multiPartMenu()
            }
        } else {
            print("Failed to generate problem. Please try again.")
        }
    }

    // MARK: - Generate Next Part
    func generateNextPart() {
        if progress.isEmpty {
            print("No multi-part problem in progress.")
            return
        }
        var currentPart = progress["current_part"] as? Int ?? 1
        currentPart += 1
        progress["current_part"] = currentPart
        let partType = progress["part_type"] as? String ?? "single-part"
        let style = progress["style"] as? String ?? "leetcode"
        let difficulty = progress["difficulty"] as? String ?? "Easy"

        let prompt = generateProblemPrompt(part: "multi", style: style, difficulty: difficulty, partNumber: currentPart)
        if let problem = callOpenAIAPI(prompt: prompt) {
            let cleanProblem = problem

            print("\nGenerated Part \(currentPart):\n\(cleanProblem)\n")

            let title = extractProblemTitle(problemContent: cleanProblem)
            let formattedTitle = formatTitleForFilename(title: "\(title)-part-\(currentPart)")
            let timestamp = getCurrentTimestamp()
            let filename = "\(formattedTitle)_\(timestamp).md"

            saveProblemToFile(problem: cleanProblem, filename: filename)

            let problemEntry: [String: Any] = [
                "problem": cleanProblem,
                "difficulty": difficulty,
                "part_type": partType,
                "style": style,
                "timestamp": timestamp,
                "filename": filename
            ]

            if var problemHistory = progress["problem_history"] as? [[String: Any]] {
                problemHistory.append(problemEntry)
                progress["problem_history"] = problemHistory
            } else {
                progress["problem_history"] = [problemEntry]
            }

            addProblemToHistory(problemEntry: problemEntry)
            saveProgress()
        } else {
            print("Failed to generate the next part. Please try again.")
        }
    }

    // MARK: - Evaluate Solution
    func evaluateSolution() {
        print("Enter the path to your Swift code .txt file: ", terminator: "")
        guard let fileName = readLine(), !fileName.isEmpty else {
            print("Invalid file name.")
            return
        }

        let fileManager = FileManager.default
        if !fileManager.fileExists(atPath: fileName) {
            print("File not found.")
            return
        }

        do {
            let swiftCode = try String(contentsOfFile: fileName, encoding: .utf8)
            print("Enter the path to the problem statement file: ", terminator: "")
            guard let problemStatementFile = readLine(), !problemStatementFile.isEmpty else {
                print("Invalid file name.")
                return
            }

            if !fileManager.fileExists(atPath: problemStatementFile) {
                print("Problem statement file not found.")
                return
            }

            let problemStatement = try String(contentsOfFile: problemStatementFile, encoding: .utf8)

            if let feedback = evaluateSwiftCode(problemStatement: problemStatement, swiftCode: swiftCode) {
                print("\nFeedback on your solution:\n\(feedback)")
            } else {
                print("Failed to evaluate the solution.")
            }

        } catch {
            print("Error reading file: \(error)")
        }
    }

    // MARK: - Evaluate Swift Code
    func evaluateSwiftCode(problemStatement: String, swiftCode: String) -> String? {
        guard let apiKey = getAPIKey() else {
            print("API key not found. Please set OPENAI_API_KEY in config.env")
            return nil
        }

        let url = URL(string: "https://api.openai.com/v1/chat/completions")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.addValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")

        let messages: [[String: Any]] = [
            [
                "role": "system",
                "content": "You are an expert coding assistant proficient in Swift and algorithm analysis."
            ],
            [
                "role": "user",
                "content": """
                I will provide you with a Swift function and a problem statement. Evaluate it based on the following criteria:

                1. **Correctness**: Is the solution correct based on the problem statement? If it is correct, state 'Correct solution.'. If the solution is incorrect, start with 'The solution is incorrect.' and then explain in detail why it is not correct based on the problem requirements.

                2. **Optimality**: If the solution is correct, evaluate whether it has the most optimal time and space complexity. If it is optimal, state 'The solution is optimal.'. If it is not, explain why it is not optimal and suggest potential improvements without revealing the full solution.

                3. **Time and Space Complexity**: Provide a time and space complexity analysis and suggest improvements if necessary.

                Please structure your evaluation using the following headings:
                - **Correctness**
                - **Optimality**
                - **Time and Space Complexity**

                **Problem Statement**:
                \(problemStatement)

                **Swift Code**:
                \(swiftCode)

                Provide your evaluation:
                """
            ]
        ]

        let body: [String: Any] = [
            "model": "gpt-4",
            "messages": messages,
            "temperature": 0
        ]

        do {
            request.httpBody = try JSONSerialization.data(withJSONObject: body, options: [])
        } catch {
            print("Error serializing request body: \(error)")
            return nil
        }

        let semaphore = DispatchSemaphore(value: 0)
        var result: String?

        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            defer { semaphore.signal() }
            if let error = error {
                print("Error during API call: \(error)")
                return
            }

            guard let data = data else {
                print("No data received from API.")
                return
            }

            do {
                if let json = try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any],
                   let choices = json["choices"] as? [[String: Any]],
                   let firstChoice = choices.first,
                   let message = firstChoice["message"] as? [String: Any],
                   let content = message["content"] as? String {
                    result = content
                } else {
                    print("Unexpected response format from API.")
                }
            } catch {
                print("Error parsing API response: \(error)")
            }
        }

        task.resume()
        semaphore.wait()

        return result
    }
}
