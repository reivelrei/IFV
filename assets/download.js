function download_old(data){
    let el = document.getElementById(data).querySelector('#plotting-area');
    el.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    console.log(data, el);

    const a = document.createElement("a");
      a.style.display = "none";
      document.body.appendChild(a);
      let type="image/svg+xml";

      // Set the HREF to a Blob representation of the data to be downloaded
      a.href = window.URL.createObjectURL(
        new Blob([el.outerHTML], { type })
      );

      // Use download attribute to set set desired file name
      a.setAttribute("download", data+'.svg');

      // Trigger the download by simulating click
      a.click();

      // Cleanup
      window.URL.revokeObjectURL(a.href);
      document.body.removeChild(a);

}

function download(data){
  let el = document.getElementById(data).querySelector('#plotting-area');
    console.log(data, el);

    const a = document.createElement("a");
      a.style.display = "none";
      document.body.appendChild(a);
      let type="image/svg+xml";

      // Set the HREF to a Blob representation of the data to be downloaded
      a.href = window.URL.createObjectURL(
        new Blob([export_StyledSVG(el)], { type })
      );

      // Use download attribute to set set desired file name
      a.setAttribute("download", data+'.svg');

      // Trigger the download by simulating click
      a.click();

      // Cleanup
      window.URL.revokeObjectURL(a.href);
      document.body.removeChild(a);



}

function read_Element(ParentNode, OrigData){
    let ContainerElements = ["svg","g"];
    let RelevantStyles = {"rect":["fill","stroke","stroke-width"],"path":["fill","stroke","stroke-width"],"circle":["fill","stroke","stroke-width"],"line":["stroke","stroke-width"],"text":["fill","font-size","text-anchor"],"polygon":["stroke","fill"]};

    let Children = ParentNode.childNodes;
    let OrigChildDat = OrigData.childNodes;

    for (let cd = 0; cd < Children.length; cd++){
        let Child = Children[cd];

        let TagName = Child.tagName;
        let className = Child.className.baseVal;
        if (ContainerElements.indexOf(TagName) !== -1){
            read_Element(Child, OrigChildDat[cd])
        } else if (TagName in RelevantStyles){
            let StyleDef = window.getComputedStyle(OrigChildDat[cd]);

            let StyleString = "";
            for (let st = 0; st < RelevantStyles[TagName].length; st++){
                StyleString += RelevantStyles[TagName][st] + ":" + StyleDef.getPropertyValue(RelevantStyles[TagName][st]) + "; ";
            }
            if(className !== 'outline_node'){
                 Child.setAttribute("style",StyleString);
            }

        }
    }

}

function export_StyledSVG(SVGElem){
    let oDOM = SVGElem.cloneNode(true)
    read_Element(oDOM, SVGElem)

    let data = new XMLSerializer().serializeToString(oDOM);
    return data;
}