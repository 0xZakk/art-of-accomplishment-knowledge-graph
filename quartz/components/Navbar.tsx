import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { classNames } from "../util/lang"

const Navbar: QuartzComponent = ({ displayClass }: QuartzComponentProps) => {
  return (
    <nav class={classNames(displayClass, "site-navbar")}>
      <div class="navbar-left">
        <a href="/" class="navbar-home">
          Home
        </a>
      </div>
      <div class="navbar-right">
        <a href="/sources/">Sources</a>
        <a href="/teachings/">Teachings</a>
        <a href="/topics/">Topics</a>
        <a href="/explore">Explore</a>
      </div>
    </nav>
  )
}

Navbar.css = `
.site-navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: min(100%, 750px);
  padding: 0.75rem 0;
  margin: 0 0 1rem 0;
  border-bottom: 1px solid var(--lightgray);
  font-size: 0.9rem;
  font-weight: 500;
}

.navbar-left a {
  color: var(--darkgray);
  text-decoration: none;
  font-weight: 600;
}

.navbar-left a:hover {
  color: var(--tertiary);
}

.navbar-right {
  display: flex;
  gap: 1.25rem;
}

.navbar-right a {
  color: var(--darkgray);
  text-decoration: none;
}

.navbar-right a:hover {
  color: var(--tertiary);
}
`

export default (() => Navbar) satisfies QuartzComponentConstructor
