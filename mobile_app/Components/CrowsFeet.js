import * as React from "react";
import { View, Text, StyleSheet } from "react-native";
import { Divider, Tooltip, Icon, Image } from "react-native-elements";
import DefaultReportView from "../Components/DefaultReportView";
import Color from "../Cons/Color";
import ImageScoreLayout from "./ImageScoreLayout";

const cf_size = ["200", "300"];
export default function CrowsFeet(props) {
  let mock_source_1 = "../images/crows1.jpg";
  let mock_source_2 = "../images/crows2.jpg";
  let mock_data = {
    "R-Crow's Feet": {
      score: "3.15",
      source: require(mock_source_1),
      height: cf_size[1],
      width: cf_size[0],
    },
    "L-Crow's Feet": {
      score: "3.5",
      source: require(mock_source_2),
      height: cf_size[1],
      width: cf_size[0],
    },
  };

  let navigation = props.navigation;
  let content = [];
  for (var key in mock_data) {
    content.push(
      <ImageScoreLayout
        source={mock_data[key]["source"]}
        key={key}
        issue={key}
        score={mock_data[key]["score"]}
        noRecommendation={true}
        height={mock_data[key]["height"]}
        width={mock_data[key]["width"]}
      />
    );
  }
  return (
    <DefaultReportView navigation={navigation} headbar="Crow's Feet Analysis">
      <View style={styles.screen}>
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

  security_level_container: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    marginBottom: 10,
  },
});
