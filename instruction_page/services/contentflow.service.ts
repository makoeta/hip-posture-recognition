import sequence from "~/content/sequence.json";

interface GuideSequence {
  urls: string[];
}

export const guideSequence: GuideSequence = {
  urls: sequence,
};
