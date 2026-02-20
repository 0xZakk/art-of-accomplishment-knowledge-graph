import { FullSlug, simplifySlug } from "../../util/path"
import type { D3Config } from "../Graph"
import type { ContentDetails } from "../../plugins/emitters/contentIndex"

type GraphControlState = {
  showTags: boolean
  showOnlySelectedTags: boolean
  hideUnrelatedPages: boolean
  tagMatchMode: "any" | "all"
  selectedTags: string[]
}

const TEACHINGS_ONLY_TYPES = ["teachings"]
const MOBILE_BREAKPOINT_QUERY = "(max-width: 800px)"

function showExploreMobileUnavailable() {
  if (document.getElementById("explore-mobile-unavailable")) return

  const center = document.querySelector("#quartz-body .center") as HTMLElement | null
  if (!center) return

  const blocker = document.createElement("section")
  blocker.id = "explore-mobile-unavailable"
  blocker.className = "explore-mobile-unavailable"
  blocker.innerHTML = `
    <div class="explore-mobile-unavailable-card">
      <h2>Explore Is Desktop-Only For Now</h2>
      <p>The interactive graph is not currently available on mobile screens.</p>
      <a href="/">Go Home</a>
    </div>
  `

  center.appendChild(blocker)
}

function findPrimaryGraph(): HTMLElement | null {
  const graphs = document.querySelectorAll(".graph")
  for (const graph of graphs) {
    if (!graph.closest(".sidebar")) {
      return graph as HTMLElement
    }
  }

  return null
}

function parseGraphConfig(container: HTMLElement): D3Config {
  return JSON.parse(container.dataset["cfg"] ?? "{}") as D3Config
}

function normalizeTag(tag: string): string {
  return simplifySlug(("tags/" + tag.trim()) as FullSlug).slice(5)
}

function parseTagList(raw: string | null): string[] {
  if (!raw) return []
  return raw
    .split(",")
    .map((tag) => normalizeTag(tag))
    .filter(Boolean)
}

function uniqueSorted(values: string[]): string[] {
  return [...new Set(values)].sort((a, b) => a.localeCompare(b))
}

function parseStateFromLocation(base: GraphControlState): GraphControlState {
  const params = new URLSearchParams(window.location.search)
  const selectedTags = uniqueSorted(parseTagList(params.get("tags")))

  const mode = params.get("match")
  const tagMatchMode: "any" | "all" = mode === "all" ? "all" : base.tagMatchMode

  const showTags = params.has("showTags") ? params.get("showTags") !== "0" : base.showTags
  const showOnlySelectedTags = params.has("selectedOnly")
    ? params.get("selectedOnly") !== "0"
    : base.showOnlySelectedTags
  const hideUnrelatedPages = params.has("relatedOnly")
    ? params.get("relatedOnly") !== "0"
    : base.hideUnrelatedPages

  return {
    showTags,
    showOnlySelectedTags,
    hideUnrelatedPages,
    tagMatchMode,
    selectedTags,
  }
}

function writeStateToLocation(state: GraphControlState) {
  const params = new URLSearchParams(window.location.search)

  if (state.selectedTags.length > 0) {
    params.set("tags", state.selectedTags.join(","))
  } else {
    params.delete("tags")
  }

  params.set("match", state.tagMatchMode)
  params.set("showTags", state.showTags ? "1" : "0")
  params.set("selectedOnly", state.showOnlySelectedTags ? "1" : "0")
  params.set("relatedOnly", state.hideUnrelatedPages ? "1" : "0")
  params.delete("types")

  const query = params.toString()
  const next = query.length > 0 ? `${window.location.pathname}?${query}` : window.location.pathname
  window.history.replaceState(window.history.state, "", next)
}

function createChip(tag: string): HTMLButtonElement {
  const chip = document.createElement("button")
  chip.className = "explore-tag-chip"
  chip.type = "button"
  chip.dataset["tag"] = tag
  chip.textContent = `#${tag} \u00d7`
  chip.title = `Remove #${tag}`
  return chip
}

function renderSelectedTags(container: HTMLElement, selectedTags: string[]) {
  container.innerHTML = ""
  if (selectedTags.length === 0) {
    const empty = document.createElement("p")
    empty.className = "explore-empty"
    empty.textContent = "No selected tags"
    container.appendChild(empty)
    return
  }

  for (const tag of selectedTags) {
    container.appendChild(createChip(tag))
  }
}

function applyStateToGraph(state: GraphControlState, graph: HTMLElement) {
  const containers = [
    graph.querySelector(".graph-container") as HTMLElement | null,
    graph.querySelector(".global-graph-container") as HTMLElement | null,
  ].filter(Boolean) as HTMLElement[]

  for (const container of containers) {
    const cfg = parseGraphConfig(container)
    cfg.showTags = state.showTags
    cfg.showOnlySelectedTags = state.showOnlySelectedTags
    cfg.hideUnrelatedPages = state.hideUnrelatedPages
    cfg.tagMatchMode = state.tagMatchMode
    cfg.selectedTags = state.selectedTags
    cfg.visibleContentTypes = [...TEACHINGS_ONLY_TYPES]
    container.dataset["cfg"] = JSON.stringify(cfg)
  }

  document.dispatchEvent(new CustomEvent("themechange", { detail: {} }))
  writeStateToLocation(state)
}

function buildBaseState(graphContainer: HTMLElement): GraphControlState {
  const cfg = parseGraphConfig(graphContainer)
  return {
    showTags: cfg.showTags,
    showOnlySelectedTags: cfg.showOnlySelectedTags ?? true,
    hideUnrelatedPages: cfg.hideUnrelatedPages ?? true,
    tagMatchMode: cfg.tagMatchMode ?? "any",
    selectedTags: cfg.selectedTags ?? [],
  }
}

async function setupExploreControls() {
  const bodySlug = document.body.dataset["slug"]
  if (bodySlug !== "explore") return

  if (window.matchMedia(MOBILE_BREAKPOINT_QUERY).matches) {
    showExploreMobileUnavailable()
    return
  }

  const graph = findPrimaryGraph()
  if (!graph) return

  const pageFooter = graph.parentElement as HTMLElement | null
  if (!pageFooter) return

  pageFooter.classList.add("explore-workspace")

  const graphContainer = graph.querySelector(".graph-container") as HTMLElement | null
  if (!graphContainer) return

  const allData = (await fetchData) as Record<string, ContentDetails>
  const allTags = uniqueSorted(Object.values(allData).flatMap((details) => details.tags ?? []))

  let state = parseStateFromLocation(buildBaseState(graphContainer))

  let panel = pageFooter.querySelector(".explore-controls-panel") as HTMLElement | null
  if (!panel) {
    panel = document.createElement("section")
    panel.className = "explore-controls-panel"
    pageFooter.prepend(panel)
  }

  panel.innerHTML = `
    <div class="explore-controls-header">
      <h3>Explore Controls</h3>
      <button type="button" class="explore-reset">Reset</button>
    </div>
    <div class="explore-control-group">
      <label for="explore-tag-input">Tag Focus</label>
      <div class="explore-tag-input-row">
        <input id="explore-tag-input" type="text" list="explore-tag-options" placeholder="Add a tag (e.g. boundaries)" />
        <button type="button" class="explore-add-tag">Add</button>
      </div>
      <datalist id="explore-tag-options"></datalist>
      <div class="explore-selected-tags"></div>
      <div class="explore-tag-actions">
        <button type="button" class="explore-hide-tags">Hide all tags</button>
        <button type="button" class="explore-show-selected">Show selected tags</button>
      </div>
    </div>
    <div class="explore-control-group">
      <label>Page Matching</label>
      <div class="explore-match-mode">
        <label><input type="radio" name="explore-match-mode" value="any" /> Any selected tag</label>
        <label><input type="radio" name="explore-match-mode" value="all" /> All selected tags</label>
      </div>
      <label><input type="checkbox" class="explore-hide-unrelated" /> Show only pages related to selected tags</label>
    </div>
    <div class="explore-control-group">
      <label>Node Visibility</label>
      <label><input type="checkbox" class="explore-show-tags" /> Show tag nodes</label>
      <label><input type="checkbox" class="explore-selected-only" /> Only show selected tag nodes</label>
    </div>
  `

  const tagInput = panel.querySelector("#explore-tag-input") as HTMLInputElement
  const addTagButton = panel.querySelector(".explore-add-tag") as HTMLButtonElement
  const hideTagsButton = panel.querySelector(".explore-hide-tags") as HTMLButtonElement
  const showSelectedButton = panel.querySelector(".explore-show-selected") as HTMLButtonElement
  const resetButton = panel.querySelector(".explore-reset") as HTMLButtonElement
  const selectedTagsContainer = panel.querySelector(".explore-selected-tags") as HTMLElement
  const datalist = panel.querySelector("#explore-tag-options") as HTMLDataListElement
  const showTagsCheckbox = panel.querySelector(".explore-show-tags") as HTMLInputElement
  const selectedOnlyCheckbox = panel.querySelector(".explore-selected-only") as HTMLInputElement
  const hideUnrelatedCheckbox = panel.querySelector(".explore-hide-unrelated") as HTMLInputElement
  const matchModeRadios = panel.querySelectorAll(
    "input[name='explore-match-mode']",
  ) as NodeListOf<HTMLInputElement>

  datalist.innerHTML = ""
  for (const tag of allTags) {
    const option = document.createElement("option")
    option.value = tag
    datalist.appendChild(option)
  }

  const syncUiFromState = () => {
    renderSelectedTags(selectedTagsContainer, state.selectedTags)
    showTagsCheckbox.checked = state.showTags
    selectedOnlyCheckbox.checked = state.showOnlySelectedTags
    hideUnrelatedCheckbox.checked = state.hideUnrelatedPages

    for (const radio of matchModeRadios) {
      radio.checked = radio.value === state.tagMatchMode
    }
  }

  const applyState = () => {
    state.selectedTags = uniqueSorted(state.selectedTags)
    syncUiFromState()
    applyStateToGraph(state, graph)
  }

  const syncFromLocation = () => {
    state = parseStateFromLocation(buildBaseState(graphContainer))
    applyState()
  }

  const addTagFromInput = () => {
    const nextTag = normalizeTag(tagInput.value)
    if (!nextTag || !allTags.includes(nextTag)) return

    if (!state.selectedTags.includes(nextTag)) {
      state.selectedTags = [...state.selectedTags, nextTag]
    }

    state.showTags = true
    state.showOnlySelectedTags = true
    state.hideUnrelatedPages = true
    tagInput.value = ""
    applyState()
  }

  const removeTag = (tag: string) => {
    state.selectedTags = state.selectedTags.filter((value) => value !== tag)
    applyState()
  }

  addTagButton.addEventListener("click", addTagFromInput)
  window.addCleanup(() => addTagButton.removeEventListener("click", addTagFromInput))

  const tagInputKeydownListener = (event: KeyboardEvent) => {
    if (event.key === "Enter") {
      event.preventDefault()
      addTagFromInput()
    }
  }
  tagInput.addEventListener("keydown", tagInputKeydownListener)
  window.addCleanup(() => tagInput.removeEventListener("keydown", tagInputKeydownListener))

  const hideTagsListener = () => {
    state.showTags = false
    applyState()
  }
  hideTagsButton.addEventListener("click", hideTagsListener)
  window.addCleanup(() => hideTagsButton.removeEventListener("click", hideTagsListener))

  const showSelectedListener = () => {
    state.showTags = true
    state.showOnlySelectedTags = true
    applyState()
  }
  showSelectedButton.addEventListener("click", showSelectedListener)
  window.addCleanup(() => showSelectedButton.removeEventListener("click", showSelectedListener))

  const resetListener = () => {
    state = {
      showTags: true,
      showOnlySelectedTags: true,
      hideUnrelatedPages: true,
      tagMatchMode: "any",
      selectedTags: [],
    }
    applyState()
  }
  resetButton.addEventListener("click", resetListener)
  window.addCleanup(() => resetButton.removeEventListener("click", resetListener))

  const showTagsChangeListener = () => {
    state.showTags = showTagsCheckbox.checked
    applyState()
  }
  showTagsCheckbox.addEventListener("change", showTagsChangeListener)
  window.addCleanup(() => showTagsCheckbox.removeEventListener("change", showTagsChangeListener))

  const selectedOnlyChangeListener = () => {
    state.showOnlySelectedTags = selectedOnlyCheckbox.checked
    applyState()
  }
  selectedOnlyCheckbox.addEventListener("change", selectedOnlyChangeListener)
  window.addCleanup(() =>
    selectedOnlyCheckbox.removeEventListener("change", selectedOnlyChangeListener),
  )

  const hideUnrelatedChangeListener = () => {
    state.hideUnrelatedPages = hideUnrelatedCheckbox.checked
    applyState()
  }
  hideUnrelatedCheckbox.addEventListener("change", hideUnrelatedChangeListener)
  window.addCleanup(() =>
    hideUnrelatedCheckbox.removeEventListener("change", hideUnrelatedChangeListener),
  )

  for (const radio of matchModeRadios) {
    const listener = () => {
      state.tagMatchMode = radio.value === "all" ? "all" : "any"
      applyState()
    }
    radio.addEventListener("change", listener)
    window.addCleanup(() => radio.removeEventListener("change", listener))
  }

  const selectedTagsClickListener = (event: Event) => {
    const target = event.target as HTMLElement
    const chip = target.closest(".explore-tag-chip") as HTMLElement | null
    if (!chip) return

    const tag = chip.dataset["tag"]
    if (!tag) return
    removeTag(tag)
  }
  selectedTagsContainer.addEventListener("click", selectedTagsClickListener)
  window.addCleanup(() =>
    selectedTagsContainer.removeEventListener("click", selectedTagsClickListener),
  )

  window.addEventListener("popstate", syncFromLocation)
  window.addCleanup(() => window.removeEventListener("popstate", syncFromLocation))

  syncUiFromState()
  applyStateToGraph(state, graph)
}

document.addEventListener("nav", () => {
  void setupExploreControls()
})
