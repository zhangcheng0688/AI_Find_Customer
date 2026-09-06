(function () {
  "use strict";

  var images = [
    {
      id: "deckcor",
      src: ((document.currentScript && document.currentScript.src) ? new URL('../images/products/slam_deck_cor_01.jpg', document.currentScript.src).href : 'assets/images/products/slam_deck_cor_01.jpg'),
      alt: "SLAM DECKCOR Bedienoberfläche"
    },
    {
      id: "scorecor",
      src: ((document.currentScript && document.currentScript.src) ? new URL('../images/products/slam_score_cor_handball_01.jpg', document.currentScript.src).href : 'assets/images/products/slam_score_cor_handball_01.jpg'),
      alt: "SLAM SCORECOR Handball-Bedienoberfläche"
    },
    {
      id: "directorcor",
      src: ((document.currentScript && document.currentScript.src) ? new URL('../images/products/slam_director_cor_01.jpg', document.currentScript.src).href : 'assets/images/products/slam_director_cor_01.jpg'),
      alt: "SLAM DIRECTORCOR Bedienoberfläche"
    },
    {
      id: "playcor",
      src: ((document.currentScript && document.currentScript.src) ? new URL('../images/products/slam_play_cor_01.jpg', document.currentScript.src).href : 'assets/images/products/slam_play_cor_01.jpg'),
      alt: "SLAM PLAYCOR Systemdarstellung"
    },
    {
      id: "timecor",
      src: ((document.currentScript && document.currentScript.src) ? new URL('../images/products/slam_time_cor_01.jpg', document.currentScript.src).href : 'assets/images/products/slam_time_cor_01.jpg'),
      alt: "SLAM TIMECOR Bedienoberfläche"
    }
  ];

  function createImage(item) {
    var image = document.createElement("img");
    image.src = item.src;
    image.alt = item.alt;
    image.width = 1920;
    image.height = 384;
    image.loading = "lazy";
    image.decoding = "async";
    image.fetchPriority = "low";
    image.className = "product-preview-image";
    image.style.display = "block";
    image.style.width = "100%";
    image.style.height = "auto";
    image.style.margin = "1.15rem 0 1.35rem";
    image.style.border = "1px solid rgba(0,0,0,0.14)";
    return image;
  }

  images.forEach(function (item) {
    var card = document.getElementById(item.id);
    var anchor = card && (card.querySelector(".product-claim") || card.querySelector("h3"));
    if (anchor) {
      anchor.insertAdjacentElement("afterend", createImage(item));
    }
  });

  var moduleHeading = Array.prototype.find.call(
    document.querySelectorAll("h3.product-name"),
    function (heading) {
      return heading.textContent.trim() === "SLAM MODULECOR";
    }
  );
  var moduleCard = moduleHeading && moduleHeading.closest("article");
  var moduleAnchor = moduleCard && (moduleCard.querySelector("p") || moduleHeading);
  if (moduleAnchor) {
    moduleAnchor.insertAdjacentElement("afterend", createImage({
      src: ((document.currentScript && document.currentScript.src) ? new URL('../images/products/slam_module_cor_01.jpg', document.currentScript.src).href : 'assets/images/products/slam_module_cor_01.jpg'),
      alt: "SLAM MODULECOR Bedienoberfläche"
    }));
  }
})();
