import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"

// components shared across all pages
export const sharedPageComponents: SharedLayout = {
  head: Component.Head(),
  header: [],
  afterBody: [
    Component.ConditionalRender({
      component: Component.Graph({
        localGraph: {
          drag: true,
          zoom: true,
          depth: 2,
          scale: 1.5,
          repelForce: 2,
          centerForce: 0.3,
          linkDistance: 50,
          fontSize: 0.4,
          focusOnHover: true,
        },
        globalGraph: {
          repelForce: 3,
          centerForce: 0.1,
          linkDistance: 60,
          fontSize: 0.5,
          focusOnHover: true,
          enableRadial: true,
        },
      }),
      condition: (page) => page.fileData.slug === "index",
    }),
    Component.ConditionalRender({
      component: Component.Graph({
        localGraph: {
          drag: true,
          zoom: true,
          depth: -1,
          scale: 0.9,
          repelForce: 3,
          centerForce: 0.3,
          linkDistance: 60,
          fontSize: 0.5,
          opacityScale: 1,
          showTags: false,
          showOnlySelectedTags: true,
          hideUnrelatedPages: true,
          visibleContentTypes: ["teachings"],
          focusOnHover: true,
          enableRadial: true,
        },
        globalGraph: {
          repelForce: 3,
          centerForce: 0.1,
          linkDistance: 60,
          fontSize: 0.5,
          visibleContentTypes: ["teachings"],
          focusOnHover: true,
          enableRadial: true,
        },
      }),
      condition: (page) => page.fileData.slug === "explore",
    }),
  ],
  footer: Component.Footer({
    links: {
      "Art of Accomplishment": "https://www.artofaccomplishment.com/",
      GitHub: "https://github.com/0xZakk/aoa-zettelkasten",
    },
  }),
}

// components for pages that display a single page (e.g. a single note)
export const defaultContentPageLayout: PageLayout = {
  beforeBody: [
    Component.Navbar(),
    Component.ConditionalRender({
      component: Component.Breadcrumbs(),
      condition: (page) => page.fileData.slug !== "index" && page.fileData.slug !== "explore",
    }),
    Component.ConditionalRender({
      component: Component.ArticleTitle(),
      condition: (page) => page.fileData.slug !== "index" && page.fileData.slug !== "explore",
    }),
    Component.ConditionalRender({
      component: Component.ContentMeta(),
      condition: (page) => page.fileData.slug !== "index" && page.fileData.slug !== "explore",
    }),
    Component.ConditionalRender({
      component: Component.TagList(),
      condition: (page) => page.fileData.slug !== "index" && page.fileData.slug !== "explore",
    }),
  ],
  left: [
    Component.ConditionalRender({
      component: Component.PageTitle(),
      condition: (page) => page.fileData.slug !== "index" && page.fileData.slug !== "explore",
    }),
    Component.ConditionalRender({
      component: Component.MobileOnly(Component.Spacer()),
      condition: (page) => page.fileData.slug !== "index" && page.fileData.slug !== "explore",
    }),
    Component.ConditionalRender({
      component: Component.Flex({
        components: [
          {
            Component: Component.Search(),
            grow: true,
          },
          { Component: Component.Darkmode() },
          { Component: Component.ReaderMode() },
        ],
      }),
      condition: (page) => page.fileData.slug !== "index" && page.fileData.slug !== "explore",
    }),
    Component.ConditionalRender({
      component: Component.Explorer(),
      condition: (page) => page.fileData.slug !== "index" && page.fileData.slug !== "explore",
    }),
  ],
  right: [
    Component.ConditionalRender({
      component: Component.Graph({
        localGraph: {
          repelForce: 2,
          centerForce: 0.5,
          linkDistance: 50,
          fontSize: 0.4,
          focusOnHover: true,
        },
        globalGraph: {
          repelForce: 3,
          centerForce: 0.1,
          linkDistance: 60,
          fontSize: 0.5,
          focusOnHover: true,
          enableRadial: true,
        },
      }),
      condition: (page) => page.fileData.slug !== "index" && page.fileData.slug !== "explore",
    }),
    Component.ConditionalRender({
      component: Component.DesktopOnly(Component.TableOfContents()),
      condition: (page) => page.fileData.slug !== "index" && page.fileData.slug !== "explore",
    }),
    Component.ConditionalRender({
      component: Component.Backlinks(),
      condition: (page) => page.fileData.slug !== "index" && page.fileData.slug !== "explore",
    }),
  ],
}

// components for pages that display lists of pages  (e.g. tags or folders)
export const defaultListPageLayout: PageLayout = {
  beforeBody: [
    Component.Navbar(),
    Component.Breadcrumbs(),
    Component.ArticleTitle(),
    Component.ContentMeta(),
  ],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Flex({
      components: [
        {
          Component: Component.Search(),
          grow: true,
        },
        { Component: Component.Darkmode() },
      ],
    }),
    Component.Explorer(),
  ],
  right: [],
}
