document.addEventListener("nav", () => {
  const placeholder = document.getElementById("homepage-graph-placeholder")
  if (!placeholder) return

  // Find the graph in afterBody (not in the sidebar)
  const afterBody = document.querySelector(".page-footer")?.previousElementSibling
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
      break
    }
  }
})
