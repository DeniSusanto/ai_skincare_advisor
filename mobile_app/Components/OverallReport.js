import * as React from "react";
import { View, Text, ActivityIndicator, StyleSheet } from "react-native";
import { Divider, Image, Tooltip, Icon } from "react-native-elements";
import DefaultReportView from "../Components/DefaultReportView";
import Color from "../Cons/Color";
import FacialIssue from "../Components/FacialIssue";
import OneImage from "./OneImageReport";

export default function Overall(props) {
  let mock_data = {
    Acne: { score: "1.3", recommendation: {} },
    Wrinkles: {
      score: "2.7",
      recommendation: {
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
      },
    },
    "Dark Eye Circle": { score: "0.3", recommendation: {} },
    "Crow's Feet": {
      score: "2.0",
      recommendation: {
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
      },
    },
    Sallowness: {
      score: "3.1",
      recommendation: {
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
    },
  };
  let mock_source = "../images/leo.png";

  let navigation = props.navigation;
  let content = [];
  for (var key in mock_data) {
    content.push(
      <FacialIssue
        key={key}
        issue={key}
        score={mock_data[key]["score"]}
        prod={mock_data[key]["recommendation"]}
      />
    );
  }
  return (
    <DefaultReportView navigation={navigation} headbar="Overall Analysis">
      <View style={styles.screen}>
        <View>
          <OneImage source={require(mock_source)} />
        </View>
        <View style={styles.security_level_container}>
          <Text style={{ fontSize: 20, fontWeight: "bold", marginRight: 6 }}>
            Severity Level
          </Text>
          <Tooltip
            containerStyle={{
              height: "auto",
              width: "auto",
            }}
            popover={
              <Text style={{ color: "white" }}>
                Score:{"\n"}0 - Clear{"\n"}1 - Almost Clear{"\n"}2 - Moderate{" "}
                {"\n"}3 - Bad {"\n"}4 - Severe
              </Text>
            }
          >
            <Icon name="info" size={26} />
          </Tooltip>
        </View>
        <Divider style={{ height: 2, width: "90%", marginBottom: 15 }} />

        {content}
      </View>
    </DefaultReportView>
  );
}
const styles = StyleSheet.create({
  screen: {
    flex: 1,
    padding: 10,
    alignItems: "center",
    backgroundColor: Color.subtle_light_grey,
  },
  report_component: {
    width: "100%",
    flex: 1,
    alignItems: "center",
  },
  security_level_container: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    marginBottom: 10,
  },
});
