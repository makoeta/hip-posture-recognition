export const useCheckListItemCounter = () => {
  return useState("checkListItemCounter", () => 0);
};
export const useCheckedCheckListItemCounter = () => {
  return useState("checkedCheckListItemCounter", () => 0);
};

export const useAllGuideItemsChecked = () => {
  const counter = useCheckListItemCounter();
  const checkedCounter = useCheckedCheckListItemCounter();
  return computed(() => {
    return counter.value == checkedCounter.value && checkedCounter.value > 0;
  });
};
