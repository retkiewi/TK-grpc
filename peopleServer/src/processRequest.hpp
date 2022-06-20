#pragma once

#include <opencv2/core/persistence.hpp>
#include <string>
#include <optional>

#include "PeopleDetector.hpp"
#include "core-people.grpc.pb.h"


bool hasPeopleFilter(size_t numberOfPeople, bool hasPeople);
bool minPeopleFilter(size_t numberOfPeople, int minPeople);
bool maxPeopleFilter(size_t numberOfPeople, int maxPeople);

bool filterImage(PeopleDetector&& peopleDetector,
                 const std::string& path,
                 bool hasPeople,
                 std::optional<int> minPeople = std::nullopt,
                 std::optional<int> maxPeople = std::nullopt);

void processRequest(const cv::FileStorage& cascadeFile,
                    const PeopleRequest* request,
                    PeopleResponse* reply);
