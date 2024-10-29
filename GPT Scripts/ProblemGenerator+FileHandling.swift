//
//  ProblemGenerator+FileHandling.swift
//  GPT Scripts
//
//  Created by TaeVon Lewis on 10/29/24.
//

import Foundation

extension ProblemGenerator {
    // MARK: - Directory Creation
    func createProblemsDirectoryIfNeeded() {
        let problemsPath = (baseDir as NSString).appendingPathComponent(problemsDir)
        if !FileManager.default.fileExists(atPath: problemsPath) {
            do {
                try FileManager.default.createDirectory(atPath: problemsPath, withIntermediateDirectories: true, attributes: nil)
                print("Created problems directory at \(problemsPath)")
            } catch {
                print("Error creating problems directory: \(error)")
            }
        }
    }

    func createHistoryProgressDirectoryIfNeeded() {
        let historyProgressPath = (baseDir as NSString).appendingPathComponent(historyProgressDir)
        if !FileManager.default.fileExists(atPath: historyProgressPath) {
            do {
                try FileManager.default.createDirectory(atPath: historyProgressPath, withIntermediateDirectories: true, attributes: nil)
                print("Created history-progress directory at \(historyProgressPath)")
            } catch {
                print("Error creating history-progress directory: \(error)")
            }
        }
    }

    // MARK: - File Paths
    func getHistoryFilePath() -> String {
        let historyDirPath = (baseDir as NSString).appendingPathComponent(historyProgressDir)
        let historyFilePath = (historyDirPath as NSString).appendingPathComponent(historyFile)
        return historyFilePath
    }

    func getProgressFilePath() -> String {
        let progressDirPath = (baseDir as NSString).appendingPathComponent(historyProgressDir)
        let progressFilePath = (progressDirPath as NSString).appendingPathComponent(progressFile)
        return progressFilePath
    }

    // MARK: - History Handling
    func loadHistory() {
        let historyFilePath = getHistoryFilePath()
        if !FileManager.default.fileExists(atPath: historyFilePath) {
            let emptyArray: [Any] = []
            do {
                let data = try JSONSerialization.data(withJSONObject: emptyArray, options: [])
                try data.write(to: URL(fileURLWithPath: historyFilePath))
                history = []
                print("Created history file at \(historyFilePath)")
            } catch {
                print("Error creating history file: \(error)")
            }
        } else {
            do {
                let data = try Data(contentsOf: URL(fileURLWithPath: historyFilePath))
                if let json = try JSONSerialization.jsonObject(with: data, options: []) as? [[String: Any]] {
                    history = json
                    print("Loaded history from \(historyFilePath)")
                }
            } catch {
                print("Error loading history: \(error)")
            }
        }
    }

    func saveHistory() {
        let historyFilePath = getHistoryFilePath()
        do {
            let data = try JSONSerialization.data(withJSONObject: history, options: [.prettyPrinted])
            try data.write(to: URL(fileURLWithPath: historyFilePath))
        } catch {
            print("Error saving history: \(error)")
        }
    }

    // MARK: - Progress Handling
    func loadProgress() {
        let progressFilePath = getProgressFilePath()
        if !FileManager.default.fileExists(atPath: progressFilePath) {
            let emptyDict: [String: Any] = [:]
            do {
                let data = try JSONSerialization.data(withJSONObject: emptyDict, options: [])
                try data.write(to: URL(fileURLWithPath: progressFilePath))
                progress = [:]
                print("Created progress file at \(progressFilePath)")
            } catch {
                print("Error creating progress file: \(error)")
            }
        } else {
            do {
                let data = try Data(contentsOf: URL(fileURLWithPath: progressFilePath))
                if let json = try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any] {
                    progress = json
                    print("Loaded progress from \(progressFilePath)")
                }
            } catch {
                print("Error loading progress: \(error)")
            }
        }
    }

    func saveProgress() {
        let progressFilePath = getProgressFilePath()
        do {
            let data = try JSONSerialization.data(withJSONObject: progress, options: [.prettyPrinted])
            try data.write(to: URL(fileURLWithPath: progressFilePath))
        } catch {
            print("Error saving progress: \(error)")
        }
    }

    func clearProgress() {
        progress = [:]
        saveProgress()
    }

    // MARK: - Problem Saving
    func saveProblemToFile(problem: String, filename: String) {
        let problemsPath = (baseDir as NSString).appendingPathComponent(problemsDir)
        let difficultyDir = (problemsPath as NSString).appendingPathComponent(currentDifficulty.lowercased())
        if !FileManager.default.fileExists(atPath: difficultyDir) {
            do {
                try FileManager.default.createDirectory(atPath: difficultyDir, withIntermediateDirectories: true, attributes: nil)
                print("Created difficulty directory at \(difficultyDir)")
            } catch {
                print("Error creating difficulty directory: \(error)")
            }
        }
        let filePath = (difficultyDir as NSString).appendingPathComponent(filename)
        do {
            try problem.write(toFile: filePath, atomically: true, encoding: .utf8)
            print("Problem saved to file: \(filePath)")
        } catch {
            print("Error saving problem to file: \(error)")
        }
    }

    // MARK: - History Management
    func addProblemToHistory(problemEntry: [String: Any]) {
        history.append(problemEntry)
        saveHistory()
    }
}
