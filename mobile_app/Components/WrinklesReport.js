import * as React from "react";
import { View, Text, StyleSheet } from "react-native";
import { Divider, Tooltip, Icon } from "react-native-elements";
import DefaultReportView from "../Components/DefaultReportView";
import Color from "../Cons/Color";
import FacialIssue from "../Components/FacialIssue";
import OneImage from "./OneImageReport";

export default function Wrinkles(routeProps) {
  let props = routeProps.route.params;
  let navigation = routeProps.navigation;
  let data_wrinkles = props.issues.Wrinkles.score;
  let data_cf = props.issues["Crow's Feet"].score;

  let wrinkle_name_mapping = {
    fh: "Forehead",
    rnl: "R - Nasal Line",
    lnl: "L - Nasal Line",
    rbe: "R - Below Eyes",
    lbe: "L - Below Eyes",
  };
  let cf_name_mapping = {
    r: "R - Crow's Feet",
    l: "L - Crow's Feet",
  };
  let content = [];
  for (var key in data_wrinkles) {
    if (key != "overall") {
      content.push(
        <FacialIssue
          key={key}
          issue={wrinkle_name_mapping[key]}
          score={data_wrinkles[key].toFixed(2)}
          noRecommendation={true}
        />
      );
    }
  }
  for (var key in data_cf) {
    if (key != "overall") {
      content.push(
        <FacialIssue
          key={key}
          issue={cf_name_mapping[key]}
          score={data_cf[key].toFixed(2)}
          noRecommendation={true}
        />
      );
    }
  }
  return (
    <DefaultReportView
      navigation={navigation}
      headbar="Wrinkles Analysis"
      routeProps={routeProps}
    >
      <View style={styles.screen}>
        <View>
          <OneImage source={{ uri: props.full_image }} />
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
