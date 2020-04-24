import * as React from "react";
import { View, Text, ActivityIndicator, StyleSheet } from "react-native";
import { Divider, Image, Tooltip, Icon } from "react-native-elements";
import DefaultReportView from "../Components/DefaultReportView";
import Color from "../Cons/Color";
import FacialIssue from "../Components/FacialIssue";
import OneImage from "./OneImageReport";
import Concern from "../Components/OtherConcerns";
import Api from "../Cons/Api";

export default function Overall(routeProps) {
  let props = routeProps.route.params;
  let navigation = routeProps.navigation;
  let concerns = JSON.parse(props.concerns);
  let issues = props.issues;
  let content = [];
  for (var key in issues) {
    content.push(
      <FacialIssue
        key={key}
        issue={key}
        score={issues[key]["score"]["overall"].toFixed(2)}
        prod={JSON.parse(issues[key]["recommendation"])}
      />
    );
  }

  let concern_content = [];
  for (var key in concerns) {
    concern_content.push(
      <Concern key={key} issue={key} prod={concerns[key]["recommendation"]} />
    );
  }

  return (
    <DefaultReportView
      navigation={navigation}
      headbar="Overall Analysis"
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

        {!(
          Object.keys(concerns).length === 0 && concerns.constructor === Object
        ) && (
          <React.Fragment>
            <Divider style={{ height: 2, width: "90%", marginVertical: 10 }} />
            <View style={styles.security_level_container}>
              <Text
                style={{ fontSize: 20, fontWeight: "bold", marginRight: 6 }}
              >
                Other Concerns
              </Text>
              <Tooltip
                containerStyle={{
                  height: "auto",
                  width: "auto",
                }}
                popover={
                  <Text style={{ color: "white" }}>
                    These are the concerns that you {"\n"}specified in the
                    questionnaire
                  </Text>
                }
              >
                <Icon name="info" size={26} />
              </Tooltip>
            </View>
            <Divider style={{ height: 2, width: "90%", marginVertical: 10 }} />
            {concern_content}
          </React.Fragment>
        )}
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
    marginVertical: 10,
  },
});
