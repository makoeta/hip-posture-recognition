interface ContentFlow {
  segments: ContentFlowSegment[];
}

interface ContentFlowSegment {
  pages: number;
  title: string;
  baseUrl: string;
}

export class ContentFlowService {
  getGuideFlow(): ContentFlow {
    return {
      segments: [
        {
          title: "toc",
          pages: 1,
          baseUrl: "/guide/toc",
        },
        {
          title: "hardware",
          pages: 4,
          baseUrl: "/guide/hardware",
        },
        {
          title: "software",
          pages: 4,
          baseUrl: "/guide/software",
        },
        {
          title: "installation",
          pages: 3,
          baseUrl: "/guide/installation",
        },
      ],
    };
  }
}
