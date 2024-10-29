//
//  ProblemGenerator+APICalls.swift
//  GPT Scripts
//
//  Created by TaeVon Lewis on 10/29/24.
//

import Foundation

extension ProblemGenerator {
    // MARK: - API Key Retrieval
    func getAPIKey() -> String? {
        let configFilePath = (baseDir as NSString).appendingPathComponent("config.env")

        print("Looking for config.env at: \(configFilePath)")

        if FileManager.default.fileExists(atPath: configFilePath) {
            do {
                let content = try String(contentsOfFile: configFilePath, encoding: .utf8)
                let lines = content.split(separator: "\n")
                for line in lines {
                    let trimmedLine = line.trimmingCharacters(in: .whitespacesAndNewlines)
                    if trimmedLine.hasPrefix("OPENAI_API_KEY=") {
                        let components = trimmedLine.components(separatedBy: "=")
                        if components.count == 2 {
                            return components[1]
                        }
                    }
                }
            } catch {
                print("Error reading config.env: \(error)")
            }
        } else {
            print("config.env not found at path: \(configFilePath)")
        }
        return nil
    }

    // MARK: - OpenAI API Call
    func callOpenAIAPI(prompt: String) -> String? {
        guard let apiKey = getAPIKey() else {
            print("API key not found. Please set OPENAI_API_KEY in config.env")
            return nil
        }

        let url = URL(string: "https://api.openai.com/v1/chat/completions")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.addValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")

        let systemMessage = [
            "role": "system",
            "content": """
            You are an expert in Apple iOS user interface engineering. Create real-world technical interview problems covering all aspects of user interface, including layout, animations, responsiveness, color contrast, user interaction, gestures, haptics, dynamic type, and anything else user interface related. Use Swift syntax and do not include a solution. Do not provide any hints or notes on what data structure and/or algorithm to use. Format the problem description in markdown. The problem must include a title, problem statement, examples, constraints, function signature, and the most optimal time and space complexity.
            """
        ]
        let userMessage = ["role": "user", "content": prompt]

        let body: [String: Any] = [
            "model": "gpt-o1-preview",
            "messages": [systemMessage, userMessage],
            "n": 1,
            "temperature": 0.7
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
