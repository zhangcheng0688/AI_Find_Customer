(function () {
  "use strict";

  var images = [
    {
      id: "cloud",
      src: "assets/images/solutions/slam_solution_cloud_01.jpg",
      alt: "SLAM.SYSTEMS Cloud"
    },
    {
      id: "training",
      src: "assets/images/solutions/slam_solution_training_01.jpg",
      alt: "SLAM.SYSTEMS Training"
    },
    {
      id: "custom-made",
      src: "assets/images/solutions/slam_solution_customade_01.jpg",
      alt: "SLAM.SYSTEMS Custom Made"
    }
  ];

  images.forEach(function (item) {
    var section = document.getElementById(item.id);
    var heading = section && section.querySelector(".content-card h3");
    if (!heading) {
      return;
    }

    var image = document.createElement("img");
    image.src = item.src;
    image.alt = item.alt;
    image.width = 1920;
    image.height = 384;
    image.loading = "lazy";
    image.decoding = "async";
    image.fetchPriority = "low";
    image.className = "solution-preview-image";
    heading.insertAdjacentElement("afterend", image);
  });

  var matcher = /SLAM\.(?:SYSTEMS|CLOUD)/;
  var splitter = /(SLAM\.(?:SYSTEMS|CLOUD))/g;
  var exactMatch = /^SLAM\.(?:SYSTEMS|CLOUD)$/;
  var walker = document.createTreeWalker(
    document.body,
    NodeFilter.SHOW_TEXT,
    {
      acceptNode: function (node) {
        var parent = node.parentElement;
        if (!parent || /^(SCRIPT|STYLE|NOSCRIPT|TEXTAREA)$/.test(parent.tagName)) {
          return NodeFilter.FILTER_REJECT;
        }
        return matcher.test(node.textContent)
          ? NodeFilter.FILTER_ACCEPT
          : NodeFilter.FILTER_REJECT;
      }
    }
  );
  var textNodes = [];
  while (walker.nextNode()) {
    textNodes.push(walker.currentNode);
  }

  textNodes.forEach(function (node) {
    var parts = node.textContent.split(splitter);
    var fragment = document.createDocumentFragment();
    parts.forEach(function (part) {
      if (!part) {
        return;
      }
      if (exactMatch.test(part)) {
        var brand = document.createElement("span");
        brand.className = "solution-brand-term";
        brand.textContent = part;
        fragment.appendChild(brand);
      } else {
        fragment.appendChild(document.createTextNode(part));
      }
    });
    node.parentNode.replaceChild(fragment, node);
  });
})();
