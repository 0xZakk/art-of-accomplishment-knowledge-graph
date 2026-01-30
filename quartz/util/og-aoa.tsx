import { SocialImageOptions, ImageOptions, UserOpts } from "./og"
import { getFontSpecificationName } from "./theme"

export const aoaOgImage: SocialImageOptions["imageStructure"] = ({
  cfg,
  userOpts,
  title,
  description,
  fonts,
  fileData,
}) => {
  const headerFont = getFontSpecificationName(cfg.theme.typography.header)
  const bodyFont = getFontSpecificationName(cfg.theme.typography.body)

  // Strip the pageTitleSuffix from title for cleaner display
  const pageTitleSuffix = cfg.pageTitleSuffix ?? ""
  const cleanTitle = pageTitleSuffix && title.endsWith(pageTitleSuffix)
    ? title.slice(0, -pageTitleSuffix.length)
    : title

  const fontBreakPoint = 30
  const useSmallerFont = cleanTitle.length > fontBreakPoint
  const useEvenSmallerFont = cleanTitle.length > 60

  return (
    <div
      style={{
        display: "flex",
        width: "100%",
        height: "100%",
        backgroundColor: "#181F2B",
        position: "relative",
      }}
    >
      {/* Orange left accent bar */}
      <div
        style={{
          display: "flex",
          position: "absolute",
          left: 0,
          top: 0,
          bottom: 0,
          width: "8px",
          backgroundColor: "#F5931C",
        }}
      />

      {/* Main content area */}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          width: "100%",
          height: "100%",
          padding: "60px 70px 50px 70px",
        }}
      >
        {/* Top section: branding */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "12px",
          }}
        >
          <div
            style={{
              display: "flex",
              width: "10px",
              height: "10px",
              borderRadius: "50%",
              backgroundColor: "#F5931C",
            }}
          />
          <div
            style={{
              display: "flex",
              fontSize: 22,
              color: "#5A6478",
              fontFamily: bodyFont,
              letterSpacing: "0.05em",
              textTransform: "uppercase",
            }}
          >
            Art of Accomplishment · Knowledge Base
          </div>
        </div>

        {/* Middle section: title + description */}
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            flex: 1,
            justifyContent: "center",
            marginTop: "20px",
          }}
        >
          <div
            style={{
              display: "flex",
              fontSize: useEvenSmallerFont ? 48 : useSmallerFont ? 56 : 66,
              fontFamily: headerFont,
              fontWeight: 700,
              color: "#F5F7FA",
              lineHeight: 1.15,
              marginBottom: description ? "24px" : "0",
            }}
          >
            {cleanTitle}
          </div>

          {description && (
            <div
              style={{
                display: "flex",
                fontSize: 26,
                color: "#8A92A4",
                fontFamily: bodyFont,
                lineHeight: 1.5,
                maxWidth: "90%",
              }}
            >
              {(() => {
                // Strip leading "Summary" that comes from the H2 heading in source pages
                let desc = description.replace(/^Summary\s*/i, "").trim()
                const truncated = desc.length > 160 ? desc.slice(0, 157) + "…" : desc
                const isSource = fileData.slug?.startsWith("sources/")
                return isSource ? "Summary: " + truncated : truncated
              })()}
            </div>
          )}
        </div>

        {/* Bottom section: orange accent line */}
        <div
          style={{
            display: "flex",
            width: "80px",
            height: "4px",
            backgroundColor: "#F5931C",
            borderRadius: "2px",
          }}
        />
      </div>
    </div>
  )
}
