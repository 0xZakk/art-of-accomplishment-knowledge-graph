document.addEventListener("nav", () => {
  const sidebar = document.querySelector(".sidebar.left") as HTMLElement
  if (!sidebar) return

  const threshold = 150

  const onScroll = () => {
    if (window.scrollY > threshold) {
      sidebar.classList.add("scrolled")
    } else {
      sidebar.classList.remove("scrolled")
    }
  }

  // Initial check
  onScroll()

  window.addEventListener("scroll", onScroll, { passive: true })
  window.addCleanup(() => window.removeEventListener("scroll", onScroll))
})
