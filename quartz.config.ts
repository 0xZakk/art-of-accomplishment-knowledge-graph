import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

/**
 * Quartz 4 Configuration
 *
 * See https://quartz.jzhao.xyz/configuration for more information.
 */
const config: QuartzConfig = {
  configuration: {
    pageTitle: "Art of Accomplishment",
    pageTitleSuffix: " · Knowledge Base",
    enableSPA: true,
    enablePopovers: true,
    analytics: {
      provider: "plausible",
    },
    locale: "en-US",
    baseUrl: "quartz.jzhao.xyz",
    ignorePatterns: ["private", "templates", ".obsidian"],
    defaultDateType: "modified",
    theme: {
      fontOrigin: "googleFonts",
      cdnCaching: true,
      typography: {
        header: "Poppins",
        body: "Poppins",
        code: "IBM Plex Mono",
      },
      colors: {
        lightMode: {
          light: "#FAFBFD",
          lightgray: "#E8EAF0",
          gray: "#A2A4B8",
          darkgray: "#3D3D3D",
          dark: "#181F2B",
          secondary: "#33465D",
          tertiary: "#F5931C",
          highlight: "rgba(245, 147, 28, 0.1)",
          textHighlight: "#F5931C44",
        },
        darkMode: {
          light: "#181F2B",
          lightgray: "#2A3347",
          gray: "#5A6478",
          darkgray: "#D4D8E0",
          dark: "#F5F7FA",
          secondary: "#F5931C",
          tertiary: "#E8852A",
          highlight: "rgba(245, 147, 28, 0.12)",
          textHighlight: "#F5931C44",
        },
      },
    },
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      Plugin.CreatedModifiedDate({
        priority: ["frontmatter", "git", "filesystem"],
      }),
      Plugin.SyntaxHighlighting({
        theme: {
          light: "github-light",
          dark: "github-dark",
        },
        keepBackground: false,
      }),
      Plugin.ObsidianFlavoredMarkdown({ enableInHtmlEmbed: false }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents(),
      Plugin.CrawlLinks({ markdownLinkResolution: "shortest" }),
      Plugin.Description(),
      // Plugin.Latex({ renderEngine: "katex" }),
    ],
    filters: [Plugin.RemoveDrafts()],
    emitters: [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.TagPage(),
      Plugin.ContentIndex({
        enableSiteMap: true,
        enableRSS: true,
      }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.Favicon(),
      Plugin.NotFoundPage(),
      // Comment out CustomOgImages to speed up build time
      // Plugin.CustomOgImages(), // temporarily disabled for fast builds
    ],
  },
}

export default config
