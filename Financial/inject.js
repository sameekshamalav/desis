function init() {
    const svgElement = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svgElement.setAttribute("width", "50");
    svgElement.setAttribute("height", "50");
    svgElement.classList.add("centered-svg"); // Add class to SVG

    // Create a circle inside the SVG
    const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    circle.setAttribute("cx", "25");
    circle.setAttribute("cy", "25");
    circle.setAttribute("r", "20");
    circle.setAttribute("fill", "blue"); // Set the circle fill color

    // Append circle to the SVG
    svgElement.appendChild(circle);

    // Style SVG for top right positioning
    svgElement.style.position = "fixed";
    svgElement.style.top = "30%";
    svgElement.style.left = "98%";
    svgElement.style.transform = "translate(-30%, -98%)";
    svgElement.style.zIndex = "9999"; // Set z-index to a high value
    svgElement.addEventListener("click", () => {
      if (chrome.runtime?.id) {
        chrome.runtime.sendMessage("OpenPopup")
      }
        
      })
    // Append SVG to the document body
    document.body.appendChild(svgElement);
    // Style el for top right positioning
    
    
}

init()