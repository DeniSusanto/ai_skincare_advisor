import * as React from "react";
import { View } from "react-native";
import Color from "../Cons/Color";
import { ScrollView } from "react-native-gesture-handler";
import CatalogueList from "../Components/CatalogueList";

export default function Recommendation(routeProps) {
  let data = JSON.parse(routeProps.route.params.full_recommendations);

  let catalogue = [];
  for (var key in data) {
    catalogue.push(<CatalogueList key={key} {...data[key]} />);
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
