import * as React from "react";
import { View, StyleSheet, Text } from "react-native";
import Color from "../Cons/Color";
import { Slider } from "react-native-elements";

function colorPicker(score) {
  if (score <= 1) {
    return "#5cdb94";
  } else if (score <= 2) {
    return "#389583";
  } else if (score <= 3) {
    return "#efd70e";
  } else {
    return "#d81a1a";
  }
}

export default function ScoreIndicator(props) {
  const [score, setScore] = React.useState(0);
  const float_score = parseFloat(props.score);
  const minScore = 0;
  const maxScore = 4;

  React.useEffect(() => {
    setTimeout(function () {
      setScore(float_score);
    }, 400);
  }, []);
  return (
    <View style={styles.container}>
      <View style={styles.inner_container}>
        <Text style={{ ...styles.issue_min_max_text, color: "green" }}>
          {minScore}
        </Text>
        <Slider
          style={{
            flex: 1,
            marginRight: 5,
            marginLeft: 5,
          }}
          disabled={true}
          animateTransitions={true}
          animationType="spring"
          minimumValue={minScore}
          maximumValue={maxScore}
          value={score}
          minimumTrackTintColor={colorPicker(score)}
          maximumTrackTintColor={Color.light_grey}
          thumbStyle={{
            width: 24,
            height: "auto",
            borderRadius: 0,
            backgroundColor: "transparent",
            borderRightWidth: 12,
            borderRightColor: "transparent",
            borderLeftWidth: 12,
            borderLeftColor: "transparent",
            borderTopWidth: 24,
            borderTopColor: "#022140",
            paddingBottom: 5,
          }}
          trackStyle={{
            height: 15,
            borderRadius: 5,
          }}
        />
        <Text style={{ ...styles.issue_min_max_text, color: "red" }}>
          {maxScore}
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  issue_min_max_text: {
    fontWeight: "bold",
    fontSize: 14,
    bottom: 10,
    height: "auto",
  },
  container: {
    width: "100%",
    alignItems: "center",
  },
  inner_container: {
    flexDirection: "row",
    width: "90%",
    alignItems: "flex-end",
    justifyContent: "center",
  },
});
