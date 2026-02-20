// @ts-ignore
import clipboardScript from "./scripts/clipboard.inline"
// @ts-ignore
import sidebarScrollScript from "./scripts/sidebar-scroll.inline"
// @ts-ignore
import homepageGraphScript from "./scripts/homepage-graph.inline"
// @ts-ignore
import exploreGraphScript from "./scripts/explore-graph.inline"
import clipboardStyle from "./styles/clipboard.scss"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

const Body: QuartzComponent = ({ children }: QuartzComponentProps) => {
  return <div id="quartz-body">{children}</div>
}

Body.afterDOMLoaded =
  clipboardScript +
  "\n" +
  sidebarScrollScript +
  "\n" +
  homepageGraphScript +
  "\n" +
  exploreGraphScript
Body.css = clipboardStyle

export default (() => Body) satisfies QuartzComponentConstructor
