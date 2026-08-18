document.querySelectorAll(".product-detail-card").forEach((card) => {
  const description = card.querySelector(".product-description");
  const featureDetails = card.querySelector(".product-details");

  if (!description) return;

  const additionalParagraphs = Array.from(description.children).slice(1);
  if (!additionalParagraphs.length && !featureDetails) return;

  const toggleGroup = document.createElement("div");
  toggleGroup.className = "product-toggle-group";

  const createToggle = (label, content) => {
    if (!content || !content.children.length) return;
    const details = document.createElement("details");
    details.className = "product-more";
    const summary = document.createElement("summary");
    summary.innerHTML = `<span>${label}</span><span class="more-arrow" aria-hidden="true">→</span>`;
    const body = document.createElement("div");
    body.className = "product-more-content";
    body.append(content);
    details.append(summary, body);
    toggleGroup.append(details);
  };

  if (additionalParagraphs.length) {
    const continuedDescription = document.createElement("div");
    continuedDescription.className = "product-description product-description-more";
    additionalParagraphs.forEach((paragraph) => continuedDescription.append(paragraph));
    createToggle("Weiterlesen", continuedDescription);
  }

  if (featureDetails) {
    const featureColumns = featureDetails.querySelector(".product-detail-columns");
    if (featureColumns) {
      const columns = Array.from(featureColumns.children);
      const keyfigures = document.createElement("div");
      keyfigures.className = "product-toggle-panel";
      if (columns[0]) keyfigures.append(columns[0]);
      createToggle("Keyfigures", keyfigures);

      const extensions = document.createElement("div");
      extensions.className = "product-toggle-panel";
      if (columns[1]) extensions.append(columns[1]);
      createToggle("Extensions", extensions);
    }
    featureDetails.remove();
  }

  description.after(toggleGroup);
});
