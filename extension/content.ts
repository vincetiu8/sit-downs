import { sendToBackground } from "@plasmohq/messaging";
import axios from "axios";
import type { PlasmoCSConfig } from "plasmo";

const removeAllTagsFromElement = (element: HTMLElement, tag: string) => {
    const tags = element.getElementsByTagName(tag);
    const tagArray = Array.from(tags);
    tagArray.forEach((tag) => {
      tag.remove();
    });
}

const removeMetadataFromElement = (element: HTMLElement) => {
    const tagsToRemove = ["script", "link", "meta", "style", "span"];
    tagsToRemove.forEach((tag) => {
      removeAllTagsFromElement(element, tag);
    });
}

const removeAllIrrelevantAttributes = (element: HTMLElement) => {
    const attributesToKeep = ["href", "src", "alt", "title"];
    const allElements = element.querySelectorAll("*");
    allElements.forEach((el) => {
        const attributes = Array.from(el.attributes);
        attributes.forEach((attr) => {
          if (!attributesToKeep.includes(attr.name)) {
            el.removeAttribute(attr.name);
            return;
          }
          if (attr.name === "src" && attr.value.substring(0, 4) === "data") {
            el.removeAttribute(attr.name);
            return;
          }
          if (attr.name === "href") {
            el.setAttribute(attr.name, attr.value.split("/").slice(0, 3).join("/"));
          }
        });
    });
    const attributes = Array.from(element.attributes);
    attributes.forEach((attr) => {
      if (!attributesToKeep.includes(attr.name)) {
        element.removeAttribute(attr.name);
      }
    });
}

const removeDivsFromString = (str: string) => {
    return str.replace(/<div.*?>/g, "").replace(/<\/div>/g, "");
}

window.addEventListener("load", async () => {
    setTimeout(() => {
        const bodyCopy = document.body.cloneNode(true) as HTMLElement;
        removeMetadataFromElement(bodyCopy);
        removeAllIrrelevantAttributes(bodyCopy);

        console.log("sending to bg")

        sendToBackground({
          name: "sendPage",
          body: {
            body: removeDivsFromString(bodyCopy.outerHTML),
            title: document.title,
            url: document.URL,
          }
      })
    }, 1000)
  })

export const config: PlasmoCSConfig = {
    matches: ["*://*/*"],
}
