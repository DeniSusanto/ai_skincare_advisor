import * as React from "react";
import {
  View,
  Text,
  StyleSheet,
  ActivityIndicator,
  ShadowPropTypesIOS,
} from "react-native";
import { Divider, Tooltip, Icon, Image } from "react-native-elements";
import DefaultReportView from "../Components/DefaultReportView";
import Color from "../Cons/Color";
import FacialIssue from "../Components/FacialIssue";

export default function ImageScoreLayout(props) {
  let int_width = parseInt(props.width);
  let int_height = parseInt(props.height);
  return (
    <View
      style={{
        width: "100%",
        justifyContent: "center",
        alignItems: "center",
        marginBottom: 20,
      }}
    >
      <View>
        <Image
          source={props.source}
          style={{ width: int_width, height: int_height }}
          PlaceholderContent={<ActivityIndicator />}
        />
      </View>
      <FacialIssue
        issue={props.issue}
        score={props.score}
        noRecommendation={true}
      />
    </View>
  );
}
