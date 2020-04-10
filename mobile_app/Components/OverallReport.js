import * as React from "react";
import { View, Text, ActivityIndicator, StyleSheet } from "react-native";
import { Divider, Image, Tooltip, Icon } from "react-native-elements";
import DefaultReportView from "../Components/DefaultReportView";
import Color from "../Cons/Color";
import FacialIssue from "../Components/FacialIssue";
import OneImage from "./OneImageReport";

export default function Overall(props) {
  let mock_data = {
    Acne: "1.3",
    Wrinkles: "2.7",
    "Dark Eye Circle": "0.3",
    "Crow's Feet": "2.0",
    Sallowness: "3.1",
  };
  let mock_source = "../images/leo.png";

  let navigation = props.navigation;
  let content = [];
  for (var key in mock_data) {
    content.push(<FacialIssue key={key} issue={key} score={mock_data[key]} />);
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
