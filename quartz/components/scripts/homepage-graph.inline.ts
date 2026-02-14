document.addEventListener("nav", () => {
  const placeholder = document.getElementById("homepage-graph-placeholder")
  if (!placeholder) return

  // Find the graph in afterBody (not in the sidebar)
  const graphs = document.querySelectorAll(".graph")
  
  for (const graph of graphs) {
    // Find the graph that's NOT in the sidebar
    if (!graph.closest(".sidebar")) {
      placeholder.innerHTML = ""
      placeholder.appendChild(graph)
      const graphOuter = graph.querySelector(".graph-outer") as HTMLElement
      if (graphOuter) {
        graphOuter.style.height = "500px"
      }
      const graphContainer = graph.querySelector(".graph-container") as HTMLElement
      if (graphContainer) {
        graphContainer.style.width = "100%"
        graphContainer.style.height = "100%"
      }
      // Trigger re-render after moving by dispatching themechange
      // The graph script listens for this and will re-render
      setTimeout(() => {
        document.dispatchEvent(new CustomEvent("themechange", { detail: {} }))
      }, 100)
      break
    }
  }
})
