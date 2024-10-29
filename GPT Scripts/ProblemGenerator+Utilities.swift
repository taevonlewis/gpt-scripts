//
//  ProblemGenerator+Utilities.swift
//  GPT Scripts
//
//  Created by TaeVon Lewis on 10/29/24.
//

import Foundation

extension ProblemGenerator {
    // MARK: - Prompt Generation
    func generateProblemPrompt(part: String = "single", style: String = "leetcode", difficulty: String = "Easy", partNumber: Int = 1) -> String {
        let dataStructure = dataStructures.randomElement() ?? "Arrays"
        let algorithm = algorithms.randomElement() ?? "Sorting"
        var uiBasePrompt = "Create a \(difficulty) \(style) \(part)-part problem focusing on iOS user interface. The problem should involve \(dataStructure) and \(algorithm), and be relevant to real-world scenarios. Use Swift syntax and do not provide a solution. Do not provide hints or any detail of what data structure or algorithm to use to solve the problem."
        if part == "multi" && partNumber > 1 {
            uiBasePrompt += " This is part \(partNumber) of the problem, building upon the previous parts."
        }
        return uiBasePrompt
    }

    // MARK: - Timestamp
    func getCurrentTimestamp() -> String {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyyMMdd_HHmmss"
        return formatter.string(from: Date())
    }

    // MARK: - Title Extraction
    func extractProblemTitle(problemContent: String) -> String {
        let lines = problemContent.components(separatedBy: .newlines)
        for line in lines {
            let trimmedLine = line.trimmingCharacters(in: .whitespacesAndNewlines)
            if trimmedLine.hasPrefix("#") {
                let title = trimmedLine.trimmingCharacters(in: CharacterSet(charactersIn: "#").union(.whitespaces))
                return title
            }
        }
        return "Untitled Problem"
    }

    // MARK: - Filename Formatting
    func formatTitleForFilename(title: String) -> String {
        var formattedTitle = title.lowercased()
        do {
            let regex = try NSRegularExpression(pattern: "[^a-z0-9]+", options: [])
            formattedTitle = regex.stringByReplacingMatches(in: formattedTitle, options: [], range: NSRange(location: 0, length: formattedTitle.count), withTemplate: "-")
            formattedTitle = formattedTitle.trimmingCharacters(in: CharacterSet(charactersIn: "-"))
        } catch {
            print("Error in regex: \(error)")
        }
        return formattedTitle
    }
}
