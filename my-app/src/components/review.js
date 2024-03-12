import React, { useState } from "react";

function RatingForm() {
  const [rating, setRating] = useState(0);
  const [showPopup, setShowPopup] = useState(false);
  const [hoveredRating, setHoveredRating] = useState(0);

  const handleStarClick = (index) => {
    setRating(index + 1);
  };

  const handleStarHover = (index) => {
    setHoveredRating(index + 1);
  };

  const handleStarLeave = () => {
    setHoveredRating(0);
  };


  return (
    <div>
      <p className="text-5xl mt-8 ml-10" style={{ marginLeft: "48%" }}>
        &#11088;{` ${rating}`}
      </p>
      <div className="rating" style={{ marginLeft: "47%", marginTop: "2%" }}>
        <input type="number" name="rating" hidden value={rating} />
        {[0, 1, 2, 3, 4].map((index) => (
          <div
            key={index}
            className={`bx ${
              index < (hoveredRating || rating) ? "bxs" : "bx"
            }-star star`}
            onClick={() => handleStarClick(index)}
            onMouseEnter={() => handleStarHover(index)}
            onMouseLeave={() => handleStarLeave()}
            style={{
              justifyContent: "center",
              alignItems: "center",
              fontSize: "24px",
              width: "6%",
              scale: "200%",
              cursor: "pointer",
            }}
          ></div>
        ))}
      </div>
      <textarea
        name="opinion"
        cols="30"
        rows="5"
        placeholder="ความคิดเห็นของคุณ..."
        className="p-7 rounded-xl border-2"
        style={{ marginLeft: "30%", marginTop: "4%", width: "50%" }}
      ></textarea>
      <div className="btn-group text-center mt-4">
        <button
          type="submit"
          className="bt submit bg-blue-500 rounded-xl  text-white"
          style={{
            paddingLeft: "3%",
            paddingRight: "3%",
            marginLeft: "50%",
            paddingTop: "4px",
            paddingBottom: "4px",
          }}
        >
          ยืนยัน
        </button>
        <div>
        <div className="flex mt-10">
          <div className="h-48 w-1/2 mr-10 border-gray-200 border-2 fit rounded-xl shadow-yellow-400 hover:shadow-2xl mt-10">
          </div>
          <div className="mt-2 ml-6">
            <h1
              style={{
                textAlign: "left",
                fontWeight: "500",
                fontSize: "120%",
                paddingTop: "5%",
              }}
            >
            </h1>
          
          </div>
          <div className="h-48 w-1/2 mr-10 border-gray-200 border-2 flex rounded-xl shadow-yellow-400 hover:shadow-2xl mt-10"></div>
          <div className="h-48 w-1/2 mr-10 border-gray-200 border-2 flex rounded-xl shadow-yellow-400 hover:shadow-2xl mt-10"></div>
        </div>

        {/* <div className="flex mt-10">
          <div className="h-48 w-1/2 mr-10 border-gray-200 border-2 fit rounded-xl shadow-yellow-400 hover:shadow-2xl mt-10"></div>
          <div className="h-48 w-1/2 mr-10 border-gray-200 border-2 flex rounded-xl shadow-yellow-400 hover:shadow-2xl mt-10"></div>
          <div className="h-48 w-1/2 mr-10 border-gray-200 border-2 flex rounded-xl shadow-yellow-400 hover:shadow-2xl mt-10"></div>
        </div> */}
        </div>
        
      </div>
    </div>
  );
}

export default RatingForm;
