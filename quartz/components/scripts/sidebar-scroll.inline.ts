document.addEventListener("nav", () => {
  const sidebar = document.querySelector(".sidebar.left") as HTMLElement
  if (!sidebar) return

  // Check if we're on the homepage
  const currentSlug =
    document.body.getAttribute("data-slug") ??
    window.location.pathname.replace(/\/+$/, "").split("/").pop() ??
    ""
  const isHomepage = currentSlug === "" || currentSlug === "index" || window.location.pathname === "/"

  if (!isHomepage) {
    // On non-homepage pages, always show sidebar items
    sidebar.classList.add("scrolled")
    return
  }

  // Homepage: scroll-based show/hide
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
