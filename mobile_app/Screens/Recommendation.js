import * as React from "react";
import { View } from "react-native";
import Color from "../Cons/Color";
import { ScrollView } from "react-native-gesture-handler";
import CatalogueList from "../Components/CatalogueList";

export default function Recommendation(props) {
  let mock_data = {
    product: {
      "1": {
        title: "Loreal White Bottle",
        issue: "Acne",
        image: {
          uri:
            "https://www.sbcskincare.co.uk/wp-content/uploads/2016/05/Vitamin-C-Skincare-Gel_500ml_MOCK_VTC152ab-02-MW_LR-256x256.jpg",
        },
        price: 20,
        rating: 3.6,
        likes: 21890,
        description:
          "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. \
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. \
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, \
sunt in culpa qui officia deserunt mollit anim id est laborum",
      },
      "2": {
        title: "The Blue Bottle Thing",
        issue: "Wrinkles",
        image: require("../images/sc2.jpg"),
        price: 140,
        rating: 4.2,
        likes: 15213,
        description:
          "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. \
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. \
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, \
sunt in culpa qui officia deserunt mollit anim id est laborum",
      },
      "3": {
        title: "Golden Pee",
        issue: "Dark Eye Circle",
        image: require("../images/sc3.jpg"),
        price: 103,
        rating: 4.6,
        likes: 14208,
        description:
          "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. \
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. \
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, \
sunt in culpa qui officia deserunt mollit anim id est laborum",
      },
    },
  };

  let catalogue = [];
  let prod = mock_data["product"];
  for (var key in prod) {
    catalogue.push(<CatalogueList key={key} {...prod[key]} />);
  }
  return (
    <ScrollView>
      <View
        style={{
          width: "100%",
          alignItems: "center",
          justifyContent: "center",
          backgroundColor: Color.primary,
        }}
      >
        {catalogue}
      </View>
    </ScrollView>
  );
}
