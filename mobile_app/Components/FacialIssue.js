import * as React from "react";
import { View, Text, StyleSheet } from "react-native";
import { Overlay, Button } from "react-native-elements";
import ScoreIndicator from "../Components/ScoreIndicator";
import Color from "../Cons/Color";
export default function FacialIssue(props) {
  const [isVisible, setisVisible] = React.useState(false);

  return (
    <React.Fragment>
      <Overlay
        isVisible={isVisible}
        windowBackgroundColor="rgba(255, 255, 255, .7)"
        overlayBackgroundColor={Color.light_grey}
        width="auto"
        height="auto"
      >
        <Text>Hello from Overlay!</Text>
      </Overlay>
      <View style={styles.report_component}>
        <View style={styles.issue_container}>
          <Text style={styles.issue_name}>{props.issue}</Text>
          {!props.noRecommendation && (
            <Button
              title="Recommendation"
              type="outline"
              titleStyle={styles.issue_reccom_button_title}
              buttonStyle={styles.issue_reccom_button}
              onPress={() => setisVisible(true)}
            />
          )}
        </View>
        <View
          style={{
            flexDirection: "row",
            justifyContent: "flex-start",
            alignItems: "center",
            width: "85%",
          }}
        >
          <Text
            style={{
              fontWeight: "bold",
              fontSize: 14,
            }}
          >
            Score: {props.score}
          </Text>
        </View>
        <View style={{ width: "100%" }}>
          <ScoreIndicator score={props.score} />
        </View>
      </View>
    </React.Fragment>
  );
}

const styles = StyleSheet.create({
  report_component: {
    width: "90%",
    flex: 1,
  },
  issue_container: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingTop: 10,
    width: "85%",
    marginBottom: 5,
  },
  issue_name: {
    fontSize: 22,
    fontWeight: "bold",
    marginRight: 14,
  },
  issue_reccom_button_title: {
    fontSize: 12,
  },
  issue_reccom_button: {
    padding: 8,
    paddingTop: 4,
    paddingBottom: 4,
    borderRadius: 20,
  },
  issue_min_max: {
    flexDirection: "row",
    width: "80%",
    alignItems: "center",
    justifyContent: "space-between",
  },
  issue_min_max_text: {
    fontWeight: "bold",
    fontSize: 16,
    bottom: 10,
  },
});
