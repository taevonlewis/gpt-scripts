//
//  ProblemGenerator.swift
//  GPT Scripts
//
//  Created by TaeVon Lewis on 10/29/24.
//

import Foundation

class ProblemGenerator {
    let historyFile = "problem_history.json"
    let progressFile = "multipart_progress.json"
    let problemsDir = "problems"
    let historyProgressDir = "history-progress"

    var history: [[String: Any]] = []
    var progress: [String: Any] = [:]
    var currentDifficulty = "Easy"

    let dataStructures = [
        "Sliding Window", "Arrays & Hashing", "Two Pointers", "Sliding Window", "Stack", "Binary Search",
        "Linked List", "Trees", "Heap/Priority Queue", "Tries", "Graphs", "Advanced Graphs"
    ]
    
    let algorithms = [
        "Searching", "Greedy", "Dynamic Programming", "Recursion", "Backtracking", "Sorting",
        "Intervals", "Math & Geometry", "Bit Manipulation"
    ]
    
    let difficultyLevels = ["Easy", "Medium", "Hard"]
    let baseDir: String

    init() {
        let sourceFileURL = URL(fileURLWithPath: #file)
        baseDir = sourceFileURL.deletingLastPathComponent().path

        print("Base directory: \(baseDir)")

        createProblemsDirectoryIfNeeded()
        createHistoryProgressDirectoryIfNeeded()
        loadHistory()
        loadProgress()
    }
}
