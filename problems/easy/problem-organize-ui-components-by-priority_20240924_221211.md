# Problem: Organize UI Components by Priority

Given an array of `UIComponents` where each `UIComponent` has a `priority` attribute, write a function to sort these components by their priority in ascending order. The `UIComponent` is a struct defined as follows:

```swift
struct UIComponent {
    let id: Int
    let name: String
    let priority: Int
}
```

You are required to implement the function `sortUIComponentsByPriority(_ components: [UIComponent]) -> [UIComponent]` that takes an array of `UIComponent` and returns a new array of `UIComponent` sorted by their priority in ascending order. If two components have the same priority, maintain their relative order as in the original array (i.e., stable sort).

### Example
```swift
let components = [
    UIComponent(id: 1, name: "Button", priority: 3),
    UIComponent(id: 2, name: "Label", priority: 1),
    UIComponent(id: 3, name: "TextField", priority: 2),
    UIComponent(id: 4, name: "ImageView", priority: 2)
]

let sortedComponents = sortUIComponentsByPriority(components)
```

### Output
```swift
[
    UIComponent(id: 2, name: "Label", priority: 1),
    UIComponent(id: 3, name: "TextField", priority: 2),
    UIComponent(id: 4, name: "ImageView", priority: 2),
    UIComponent(id: 1, name: "Button", priority: 3)
]
```

### Constraints
- The number of UIComponents will not exceed 10^5.
- Each `UIComponent` will have a unique `id`.
- The `priority` attribute will be a non-negative integer.

### Function Signature
```swift
func sortUIComponentsByPriority(_ components: [UIComponent]) -> [UIComponent]
```